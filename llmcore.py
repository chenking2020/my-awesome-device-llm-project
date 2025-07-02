import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, WebSocket, File, UploadFile

from opencc import OpenCC
from llama_cpp import Llama


import numpy as np
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import datetime
from whispercppy import Whisper
import ffmpeg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

n_ctx_llm = 2048
n_ctx_vllm = 2048
multi_round = 2


messages = None

stop_flag = {}
stop_vl_flag = {}
default_user_id = "DefaultX1"

qa_prompt = (
    "上下文信息如下：\n"
    "---------------------\n"
    "{}\n"
    "---------------------\n"
    "给定以上的上下文信息, "
    "请回答我的问题：\n"
    "问题: {}\n"
    "答案: "
)

llm_path = os.path.join(BASE_DIR, "models/my_device_llm_v1.gguf")
sp_path = os.path.join(BASE_DIR, "models/my-asr-model-base.bin")
llm = None
messages = None
cc = None

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_now_str():
    timenow = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    now_time_str = timenow.strftime("%Y-%m-%d %H:%M:%S")
    return now_time_str


@app.get("/")
async def root():
    return {"message": "欢迎使用移动终端版大模型对话机器人！"}


@app.post("/chatmt/v1/asr/")
async def get_speech_text(file: UploadFile = File(...)):
    global whisper, cc
    try:
        tmp_file_path = os.path.join(BASE_DIR, "tmp.wav")
        with open(tmp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        y, _ = (
            ffmpeg.input(
                tmp_file_path,
                threads=0,
            )
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
            .run(
                cmd=["ffmpeg", "-nostdin"],
                capture_stdout=True,
                capture_stderr=True,
            )
        )
        arr = np.frombuffer(y, np.int16).flatten().astype(np.float32) / 32768.0
        return {
            "code": 200,
            "message": "successfully",
            "result": cc.convert(whisper.transcribe(arr)),
        }
    except:
        return {
            "code": 500,
            "message": " Internal Server Error‌",
            "result": "",
        }


@app.websocket("/chatmt/v1/llmchat/")
async def get_llm_chat(websocket: WebSocket):
    global llm, messages, vlllm
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        if "user_id" in data:
            if not isinstance(data["user_id"], str):
                user_id = str(data["user_id"])
            else:
                user_id = data["user_id"]
        else:
            user_id = default_user_id
        mode = "chat"
        if "mode" in data and data["mode"] == "think":
            mode = data["mode"]
            data["instruct"] = data["instruct"] + " /think"
        else:
            data["instruct"] = data["instruct"] + " /no_think"
        # 根据用户传过来的上下文进行理解问答
        if "contexts" in data and len(data["contexts"]) > 0:
            inputMes = qa_prompt.format("\n\n".join(data["contexts"]), data["instruct"])
            if len(inputMes) > n_ctx_llm:
                context_str = "\n\n".join(data["contexts"])
                cut_context_str = context_str[
                    : n_ctx_llm - len(qa_prompt) - len(data["instruct"]) - 100
                ]
                inputMes = qa_prompt.format(cut_context_str, query_str=data["instruct"])
        else:
            inputMes = data["instruct"]
            if len(inputMes) > n_ctx_llm:
                inputMes = inputMes[:n_ctx_llm]

        if (
            messages is None
            or len(messages) == 0
            or ("reset" in data and data["reset"] == 1)
        ):
            messages = [
                {"role": "user", "content": inputMes},
            ]
        elif len(messages) < multi_round * 2:
            messages.append({"role": "user", "content": inputMes})
        else:
            messages = messages[-multi_round * 2 :] + [
                {"role": "user", "content": inputMes}
            ]

        full_answer = ""
        for chunk in llm.create_chat_completion(
            messages=messages, temperature=0.1, stream=True
        ):
            if user_id in stop_flag and stop_flag[user_id]:
                break
            if "content" in chunk["choices"][0]["delta"]:
                if (
                    mode == "think"
                    and len(full_answer) == 0
                    and chunk["choices"][0]["delta"]["content"] != "<think>"
                ):
                    if user_id == default_user_id:
                        await websocket.send_json(
                            {
                                "data": "<think>",
                                "end": False,
                            }
                        )
                    else:
                        await websocket.send_json(
                            {
                                "user_id": user_id,
                                "data": "<think>",
                                "end": False,
                            }
                        )
                if (
                    mode == "chat"
                    and len(full_answer) == 0
                    and chunk["choices"][0]["delta"]["content"]
                    in ["<think>", "\n\n", "</think>"]
                ):
                    continue
                if user_id == default_user_id:
                    await websocket.send_json(
                        {
                            "data": chunk["choices"][0]["delta"]["content"],
                            "end": False,
                        }
                    )
                else:
                    await websocket.send_json(
                        {
                            "user_id": user_id,
                            "data": chunk["choices"][0]["delta"]["content"],
                            "end": False,
                        }
                    )
                await asyncio.sleep(0.000001)
                full_answer += chunk["choices"][0]["delta"]["content"]
        if user_id in stop_flag:
            stop_flag[user_id] = False
        if user_id == default_user_id:
            await websocket.send_json({"data": "--------【结束】--------", "end": True})
        else:
            await websocket.send_json(
                {"user_id": user_id, "data": "--------【结束】--------", "end": True}
            )
        messages.append(
            {"role": "assistant", "content": full_answer.split("</think>")[-1]}
        )


@app.get("/chatmt/v1/stop/")
async def stop_chat(user_id=default_user_id):
    if not isinstance(user_id, str):
        user_id = str(user_id)
    stop_flag[user_id] = True
    return {"message": "已结束对话！"}


def main():
    global llm, whisper, tts, cc
    n_workers = 1
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-nworkers":
            try:
                n_workers = int(sys.argv[i + 1])
            except:
                n_workers = 1

    cc = OpenCC("t2s")

    try:
        llm = Llama(
            model_path=llm_path,
            n_ctx=n_ctx_llm + 200,
            chat_format="chatml",
            n_gpu_layers=-1,
        )
    except:
        llm = None
        print("语言大模型加载失败")

    try:
        whisper = Whisper.from_pretrained(sp_path)
        whisper.params.language = "zh"
    except:
        whisper = None
        print("语音大模型加载失败")

    uvicorn.run(
        app, host="0.0.0.0", port=8000, workers=n_workers, timeout_keep_alive=600
    )
