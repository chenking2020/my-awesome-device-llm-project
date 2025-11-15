<template>
	<view class="chat" @touchstart="start" @touchend="end">
		<scroll-view :style="{height: `${windowHeight-inputHeight}rpx`}" id="scrollview" scroll-y="true"
			:scroll-top="scrollTop" class="scroll-view">
			<!-- 聊天主体 -->
			<view id="msglistview" class="chat-body">
				<!-- 聊天记录 -->
				<view v-for="(item,index) in msgList" :key="index">
					<!-- 自己发的消息 -->
					<view class="item self" v-if="item.role == 'human'">
						<!-- 文字内容 -->
						<view v-if="item.type && item.type == 'audio'" class="message-container">
							<view class="message" @tap="playVoice(item.src)">
								<!-- 音频 -->
								<!-- <view class="msg-text voice" :style="{width:'100'+'rpx'}"> -->
								{{item.time}}″
								<image src="../../static/audio.png" class="voice-img"></image>
								<!-- </view> -->
							</view>
						</view>
						<view v-if="item.type && item.type == 'image'" class="message-container">
							<image @longtap="longtap(item)" style="width: 200px; height: 200px; background-color: #eeeeee;" mode="aspectFit" :src="item.src" @error="imageError"></image>
						</view>
						<view v-else class="content right" @touchstart="tapTouchStart"
							@touchend="tapTouchEnd(index, $event)">
							{{item.content}}
						</view>
						<!-- 头像 -->
						<image class="avatar" :src="item.image1">
						</image>
					</view>
					<!-- 机器人发的消息 -->
					<view class="item Ai" v-if="item.role == 'robot'">
						<!-- 头像 -->
						<image class="avatar" src="../../static/img/20240722104326.jpg">
						</image>
						<!--判断是文本还是语音-->
						<view v-if="item.type && item.type === 'audio'">
							这是一段语音
							<!-- 							<audio style="text-align: left" :src="current.src" :poster="current.poster"
								:action="audioAction" controls></audio> -->
						</view>
						<!-- 文字内容 -->
						<view v-else class="content left" 
						:class="{'think-mode': item.isThink}" @touchstart="tapTouchStart"
						@touchend="tapTouchEnd(index, $event)">
							<text>
								 <view v-if="item.currentThinkContent" class="think-container">
									<view class="think-header" @click="toggleThinkingCollapse(index)">
										<text class="think-label">
											<text v-if="item.isThink && chat" class="thinking-indicator">🤔 思考中</text>
											<text v-else>🤔 深度思考过程：</text>
										</text>
										<text class="think-collapse-icon">{{ item.isThinkCollapsed ? '展开' : '收起' }}</text>
									</view>
									<view class="think-content" v-show="!item.isThinkCollapsed">
										<text>{{item.currentThinkContent}}</text>
										<text v-if="item.isThink && chat" class="thinking-cursor">|</text>
									</view>
								</view>
								{{item.content}}
							</text>
						</view>
					</view>
				</view>
			</view>
		</scroll-view>
		<view class="record-container" v-if="isRecording">
			<view class="record-logo">
				录音中...{{time}}"
			</view>
		</view>
		<!-- 用来占位，防止聊天消息被发送框遮挡 -->
		<view class="chat-bottom">
			<view class="send-msg">
				<!-- 修改语音/文本切换按钮 -->
				<view class="action-btn">
					<button 
						size="mini" 
						type="default"
						style="color:#7F7F7F;"
						hover-class="is-hover" 
						@click="changeContent">
						<text v-if="isAudio" class="iconfont">✏️</text>
						<text v-else class="iconfont">🎤</text>
					</button>
				</view>
				<!-- 输入框区域 -->
				<view class="uni-textarea" v-if="!isAudio">
					<!--显示照片提示框-->
					<view class="atta-image" v-if="chattingImage && !chat && choosed">
						<view>[图片]</view>
						<view class="atta-image-close" @click="chattingImage=''">x</view>
					</view>
					<button v-if="!isAudio && chat == true" type="primary" size="mini" maxlength="300" 
						style="width: 400rpx;height: 70rpx;line-height: 70rpx;font-size: 30rpx;font-weight: 500;"
						@click="handleStop" class="send-btn">终止</button>
					<textarea v-else v-model="chatMsg" maxlength="300" 	confirm-type="send" @confirm="handleSend"
						:show-confirm-bar="false" :adjust-position="false" @linechange="sendHeight"
						@focus="focus" @blur="blur" auto-height></textarea>
				</view>
				<view class="uni-textarea" v-else>
					<button v-if="chat == false" type="primary" size="mini" maxlength="300"
						style="width: 400rpx;height: 70rpx;line-height: 70rpx;font-size: 30rpx;font-weight: 600;color:rgba(0, 0, 0, .9);"
						@longpress="longPress" @touchend="touchEnd" @touchmove="touchMove" @click="open">按住说话</button>
					<button v-else type="primary" size="mini" maxlength="300"
						style="width: 400rpx;height: 70rpx;line-height: 70rpx;font-size: 30rpx;font-weight: 500;"
						@click="handleStop">终止</button>
				</view>
				<!-- 修改清空按钮 -->
				<button type="default" @click="newDialog(greeting)" class="action-btn">
					<text class="clear-icon">🗑️</text>
				</button>
				<!-- 修改更多按钮 -->
				<button type="default" @click="toggleMoreMenu" class="action-btn more-btn">
					<text class="more-icon">+</text>
				</button>
			</view>
			
			<!-- 更多菜单 - 底部弹出 -->
			<view class="more-menu-container" v-if="showMoreMenu">
				<view class="more-menu">
					<view class="menu-item" @click="imageChat">
						<view class="menu-icon">📷</view>
						<text>照片</text>
					</view>
					<view class="menu-item" @click="toggleThinkMode">
						<view class="menu-icon" :class="{'active-mode': isThinkMode}">🤔</view>
						<text>{{isThinkMode ? '标准模式' : '深度思考'}}</text>
					</view>
				</view>
			</view>
		</view>
		<view v-if="showFile" class="animation-class">
			<!-- 自定义弹窗效果 -->
			<view class="Popup">
				<uni-section title="文档库" type="line">
					<template v-slot:right>
						<button class="mini-btn" type="primary" size="mini" @click="inputDialogToggle">新增</button>
					</template>
					<uni-list>
						<uni-list-item v-for="(item, index) in listkbs" :key="index">
							<template v-slot:header>
								<view class="slot-box">
									<image class="slot-image" src="/static/logo.png" mode="widthFix"></image>
								</view>
							</template>
							<template v-slot:body>
								<text class="slot-box slot-text"
									@click="choose(item.id, item.name)">{{item.name | capitalize}}</text>
							</template>
							<template v-slot:footer>
								<button class="mini-btn btn-class" type="primary" @click="uploadDoc(item.id)"
									size="mini">上传</button>&nbsp;&nbsp;&nbsp;
								<button class="mini-btn btn-class" type="primary"
									@click="attachment(item.id, item.name)" size="mini">附件</button>&nbsp;&nbsp;&nbsp;
								<button class="mini-btn btn-class" type="primary" @click="deleteKbs(item.id)"
									size="mini">删除</button>&nbsp;&nbsp;&nbsp;
							</template>
						</uni-list-item>
					</uni-list>
				</uni-section>
			</view>
		</view>
		<view>
			<!-- 输入框示例 -->
			<uni-popup ref="inputDialog" type="dialog">
				<uni-popup-dialog ref="inputClose" mode="input" title="知识库名称" value="" placeholder="请输入知识库名称"
					@confirm="dialogInputConfirm"></uni-popup-dialog>
			</uni-popup>
		</view>
	</view>
</template>
<script>
	import { pathToBase64, base64ToPath } from 'image-tools'

	const recorderManager = uni.getRecorderManager();
	const innerAudioContext = uni.createInnerAudioContext();
	innerAudioContext.autoplay = true;
	
	const url1 = "ws://127.0.0.1:8005/chatmt/v1/llmchat/";
	const url2 = "ws://127.0.0.1:8005/chatmt/v1/vlchat/";
	
	let socketTask = null;
	let reconnectTimer;
	let reconnectAttempts = 0;
	const maxReconnectAttempts = 5; // 最大重连次数
	let messageQueue = []; // 消息队列用于缓存未发送的数据

	export default {
		name: "Chat",
		data() {
			return {
				// 欢迎信息
				greeting: "你好，欢迎使用，我除了支持输入文字，你也可以语音问我，也可以点击+，选择拍照问答或者深度思考问答。",
				// 新增思考模式状态
				isThinkMode: false,
				isThinking: false,
				pager: {
					page: 1,
					size: 10
				},
				id: 0,
				showFile: false,
				listkbs: [],
				tapData: {
					clientX: 0,
					clientY: 0
				},
				startData: {
					clientX: 0,
					clientY: 0
				},
				//键盘高度
				keyboardHeight: 0,
				//底部消息发送高度
				bottomHeight: 0,
				//滚动距离
				scrollTop: 0,
				userId: '',
				//发送的消息
				chatMsg: "",
				robotMsg: "",
				msgList: [{
					content: "你好，欢迎使用，我除了支持输入文字，你也可以语音问我，也可以点击+，选择拍照问答或者深度思考问答。",
					role: "robot",
					type: "string"
				}],
				isAudio: false,
				isRecording: false,
				voicePath: '',
				current: {
					poster: '../../static/audio.png',
					src: '',
				},
				audioAction: {
					method: 'pause'
				},
				first: true,
				choosed: false, //人工是否选中了图片
				time: 0,
				greettimer: null,
				timer: null,
				chat: false ,//是否正在聊天
				chattingImage:'',
				needContinue: false, //是否需要继续
				showMoreMenu: false, // 新增控制更多菜单显示/隐藏的状态
			}
		},
		updated() {
			//页面更新时调用聊天消息定位到最底部
			this.scrollToBottom();
		},
		filters: {
			capitalize: function(value) {
				if (!value) return ''
				value = value.toString()
				return value.substring(0, 20);
			}
		},
		computed: {
			windowHeight() {
				return this.rpxTopx(uni.getSystemInfoSync().windowHeight)
			},
			// 键盘弹起来的高度+发送框高度
			inputHeight() {
				return this.bottomHeight + this.keyboardHeight
			}
		},
		onLaunch: function(options) {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('页面显示，检查WebSocket状态');
			if(this.first == false && this.needContinue) {
				console.log('非正常断开，需要重连');
				if (!socketTask || socketTask.readyState === 3) { // WebSocket关闭时重新连接
					console.log('WebSocket未连接，重新连接');
					var that = this;
					let url = "";
					if(this.chattingImage) {
						url = url2;
					} else {
						url = url1;
					}
					socketTask = uni.connectSocket({
						url: url,
						success: (res) => {
							console.log('WebSocket 重连连接成功');
							if(that.chattingImage) {
								uni.showLoading({
									title: '思考中...'
								})
							}
						}
					});
				} else {
					console.log('WebSocket已重新连接');
				}
			} else {
				console.log('WebSocket默认分支,不需要重连');
			}
		},
		onLoad(option) {
			uni.onKeyboardHeightChange(res => {
				//这里正常来讲代码直接写
				//this.keyboardHeight=this.rpxTopx(res.height)就行了
				//但是之前界面ui设计聊天框的高度有点高,为了不让键盘和聊天输入框之间距离差太大所以我改动了一下。
				this.keyboardHeight = this.rpxTopx(res.height)
				if (this.keyboardHeight < 0) this.keyboardHeight = 0;
			})

			//是否第一次加载
			this.first = true;
			if (option && option.showFile) {
				this.showFile = option.showFile;
				this.getList();
			}
		},
		onUnload() {
			this.endChatSession();
			// uni.closeSocket();
			// uni.offKeyboardHeightChange()
		},
	methods: {
			// 切换思考内容的折叠状态
			toggleThinkingCollapse(index) {
				// 如果没有折叠状态属性，先初始化为false
				if (typeof this.msgList[index].isThinkCollapsed === 'undefined') {
					this.$set(this.msgList[index], 'isThinkCollapsed', false);
				}
				// 切换折叠状态
				this.$set(this.msgList[index], 'isThinkCollapsed', !this.msgList[index].isThinkCollapsed);
			},
			longtap(row){
				let that = this;
				uni.showModal({
					content: '对该照片提问?',
					confirmText: '确定',
					cancelText: '取消',
					success: function(res) {
						if (res.confirm) {
							//记录提问的照片
							that.chattingImage = row.src;
							//切换聊天内容到文字聊天
							that.isAudio = false;
							that.id = 0;
							
							that.choosed = true;
						}
					}
				});
			},
			imageError: function(e) {
				console.error('image发生error事件，携带值为' + e.detail.errMsg)
			},
			tapTouchStart(e) {
				this.tapData.clientX = e.changedTouches[0].clientX;
				this.tapData.clientY = e.changedTouches[0].clientY;
			},
			tapTouchEnd(index, e) {
				const subX = e.changedTouches[0].clientX - this.tapData.clientX;
				const subY = e.changedTouches[0].clientY - this.tapData.clientY;
				if (subY > 10 || subY < -10) {
					console.log('滑动,不做处理');
				} else {
					console.log('原微信分享逻辑');
				}
			},
			handleStop() {
				this.needContinue = false;//websocket链接不需要断开重连
				
				let url = "";
				if(this.chattingImage) {
					url = "http://127.0.0.1:8005/chatmt/v1/vlstop/"
				} else {
					url = "http://127.0.0.1:8005/chatmt/v1/stop/";	
				}
				uni.request({
					url: url,
					success: (res) => {
						let data = res.data;
						console.log('http 接口返回 : ', data);
						//最后一行为空的时候，追加接口结束提示
						if(!!!this.msgList[this.msgList.length-1].content) {
							this.msgList[this.msgList.length-1].content = data.message;
						}
						//追加终止对话提示
						let obj = {
							content: data.message,
							role: "robot",
							type: "string"
						}
						this.msgList.push(obj);
						this.chat = false;
						uni.hideLoading();
					},
					fail: (res) => {
						console.log('接口调用失败');
						this.chat = false;
						uni.hideLoading();
						//关闭websocket链接
						this.endChatSession();
					}
				});
			},
			choose(id, name) {
				this.showFile = false;
				this.chat = false;
				this.newDialog(`您选择了名称为'${name}'的知识库，你可以对该知识库发起新的话题了!`, id);
			},
			attachment(id, name) {
				//在起始页面跳转到test.vue页面并传递参数
				uni.navigateTo({
					url: `/pages/attachment/attachment?id=${id}&name=${name}`
				});
			},
			uploadDoc(id) {
				let url = 'http://127.0.0.1:8005/chatmt/v1/upload_doc/?id=' + id;
				uni.chooseImage({
					success: (chooseImageRes) => {
						uni.showLoading({
							title: '数据上传中'
						})

						const tempFilePaths = chooseImageRes.tempFilePaths;
						uni.uploadFile({
							url: url, //仅为示例，非真实的接口地址
							filePath: tempFilePaths[0],
							name: 'files',
							success: (uploadFileRes) => {
								console.log(uploadFileRes.data);
								uni.hideLoading(); //隐藏加载状态
								this.getList(); //刷新数据
							}
						});
					}
				});
			},
			//图片问答
			imageChat() {
				// 关闭更多菜单
				this.showMoreMenu = false;
				
				let that = this;
				uni.chooseImage({
					success: (chooseImageRes) => {
						const tempFilePaths = chooseImageRes.tempFilePaths;
						
						//向聊天记录推送数据
						let obj = {
							content: "",
							src: tempFilePaths[0],
							role: "human",
							type: "image"
						};
						that.msgList.push(obj);
						
						//记录提问的照片
						that.chattingImage = tempFilePaths[0];
						//切换聊天内容到文字聊天
						that.isAudio = false;
						that.id = 0;
						
						this.choosed = false;
					}
				});
			},
			deleteKbs(id) {
				uni.showLoading({
					title: '数据请求中'
				})

				const url = "http://127.0.0.1:8005/chatmt/v1/delete_kb/";
				uni.request({
					url: url,
					data: {
						id: id
					},
					header: {
						'custom-header': 'hello' //自定义请求头信息
					},
					success: (res) => {
						uni.hideLoading();

						this.pager.page = 1;
						this.getList();
					},
					fail: (res) => {
						uni.hideLoading();
					}
				});
			},
			//获取数据列表
			getList() {
				uni.showLoading({
					title: '数据请求中'
				})

				const url = "http://127.0.0.1:8005/chatmt/v1/listkbs/";
				uni.request({
					url: url,
					data: {
						page_num: this.pager.page,
						page_size: this.pager.size
					},
					header: {
						'custom-header': 'hello' //自定义请求头信息
					},
					success: (res) => {
						let data = res.data;
						if (this.pager.page == 1) {
							this.listkbs = data.data;
						} else {
							for (let i in data.data) {
								this.listkbs.push(data.data[i]);
							}
						}
						uni.hideLoading();
					},
					fail: (res) => {
						uni.hideLoading();
					}
				});
			},
			//点击了确认框事件
			dialogInputConfirm(val) {
				uni.showLoading({
					title: '数据请求中'
				})

				const url = "http://127.0.0.1:8005/chatmt/v1/create_kb";
				uni.request({
					url: url,
					data: {
						name: val
					},
					header: {
						'custom-header': 'hello' //自定义请求头信息
					},
					success: (res) => {
						let data = res.data;

						uni.hideLoading();
						this.$refs.inputDialog.close();

						this.getList(); //刷新数据
					},
					fail: (res) => {
						uni.hideLoading();
					}
				});
			},
			inputDialogToggle() {
				this.$refs.inputDialog.open()
			},
			change(e) {
				this.show = e.show
			},
			start(e) {
				this.startData.clientX = e.changedTouches[0].clientX;
				this.startData.clientY = e.changedTouches[0].clientY;
			},
			end(e) {
				// console.log(e)
				const subX = e.changedTouches[0].clientX - this.startData.clientX;
				const subY = e.changedTouches[0].clientY - this.startData.clientY;
				if (subY > 50 || subY < -50) {
					console.log('上下滑')
					//判断是否是刷新数据
					if (subY < -50 && this.showFile) {
						this.pager.page++;
						this.getList();
					}
				} else {
					if (subX > 100) {
						this.showFile = true;
						this.getList();
					} else if (subX < -100) {
						this.showFile = false;
					} else {
						console.log('无效')
					}
				}
			},
			//内容分享
			onShare(index, e) {
				const that = this;
				uni.showModal({
					content: '分享给微信好友?',
					confirmText: '确定',
					cancelText: '取消',
					success: function(res) {
						if (res.confirm) {
							const summary = that.msgList[index].content;
							uni.share({
								provider: "weixin",
								scene: "WXSceneSession",
								type: 1,
								summary: summary,
								success: function(res) {
									console.log("success:" + JSON.stringify(res));
								},
								fail: function(err) {
									console.log("fail:" + JSON.stringify(err));
								}
							});
						}
					}
				});
			},
			playVoice(voicePath) {
				if (voicePath) {
					innerAudioContext.src = voicePath;
					innerAudioContext.play();
				}
			},
			longPress(itemCode) {
				this.isRecording = true;
				this.time = 0;
				recorderManager.start({
                    format:'mp3'// 录音保存的文件格式
                });
				let that = this;

				this.timer = setInterval(function() {
					// 放入你自己的业务逻辑代码
					that.time++;
				}, 1000);
			},
			touchEnd() {
				this.isRecording = false;
				clearInterval(this.timer);
				this.timer = null;

				//停止录音
				recorderManager.stop();
				let self = this;
				recorderManager.onStop(function(res) {
					self.voicePath = res.tempFilePath;
					self.current.src = res.tempFilePath;

					//向聊天记录推送数据
					let obj = {
						content: "",
						src: res.tempFilePath,
						role: "human",
						type: "audio",
						time: self.time
					};
					self.msgList.push(obj);

					//发送http请求，调用语音识别接口
					self.upload(res.tempFilePath);
				});

				//发送音频声效
				this.playVoice('../../static/audio/SendMessage.mp3');
			},
			 upload(path) {
				uni.showLoading({
					title: "识别中...."
				});
				let that = this;
				const url = "http://127.0.0.1:8005/chatmt/v1/asr/"; //'http://127.0.0.1:8005:80/chatmt-api/v1/asr'
				uni.uploadFile({
					url: url, //改成你要传的地址，这里只是示例地址
					filePath: path,
					name: 'file', //文件对应的key
					formData: {
						'user': 'test'
					}, //HTTP 请求中其他额外的 form data |
					success: (response) => {
						console.log(response);
						uni.hideLoading();

						let data = response.data;
						let json = JSON.parse(data);
						let result = json.result;
						if(result) {
							let latestMsg = that.msgList[that.msgList.length - 1];
							latestMsg.content += result;
							
							//发送到聊天接口，添加input_type=audio参数
							that.chat = true;
							console.log('即将调用upload');
							that.chatExample(that, result, url1, 'audio');	
						} else {
							console.log('内容返回空');
						}
					},
					fail: (err) => {
						console.log('请求失败:', err);
						uni.hideLoading();
						uni.showToast({
							title: '接口请求失败!',
							duration: 2000
						});
					}
				});
			},
			onStop() {
				console.log('回调函数onStop');
			},
			touchMove(e) {
				console.log('touchMove');
				// 手指触摸后的移动事件
			},
			open() {
				console.log(this.$refs.popup);
			},
			changeContent() {
				this.isAudio = !this.isAudio;
			},
			focus() {
				this.scrollToBottom()
			},
			blur() {
				this.scrollToBottom()
			},
			// px转换成rpx
			rpxTopx(px) {
				let deviceWidth = uni.getSystemInfoSync().windowWidth
				let rpx = (750 / deviceWidth) * Number(px)
				return Math.floor(rpx)
			},
			// 监视聊天发送栏高度
			sendHeight() {
				setTimeout(() => {
					let query = uni.createSelectorQuery();
					query.select('.send-msg').boundingClientRect()
					query.exec(res => {
						this.bottomHeight = this.rpxTopx(res[0].height)
					})
				}, 10)
			},
			// 滚动至聊天底部
			scrollToBottom(e) {
				setTimeout(() => {
					let query = uni.createSelectorQuery().in(this);
					query.select('#scrollview').boundingClientRect();
					query.select('#msglistview').boundingClientRect();
					query.exec((res) => {
						if (res[1].height > res[0].height) {
							this.scrollTop = this.rpxTopx(res[1].height - res[0].height)
						}
					})
				}, 15)
			},
			newDialog(content, id) {
				//清空聊天记录
				this.msgList = [{
					content: content,
					role: "robot",
					type: "string"
				}];
				//清空聊天输入框
				this.chatMsg = "";
				this.first = true;
				this.chattingImage = "";
				this.id = id || 0;
				
				//是否选中图片清空
				this.choosed = false;
				this.chat = false;
			},
			async startChatSession(url, data) {
				var that = this;
			    return new Promise((resolve, reject) => {
			        // 1. 创建WebSocket连接
			        socketTask = uni.connectSocket({
			            url: url,
			            success: () => {
			                console.log("WebSocket 连接成功");
			            },
			            fail: (err) => {
			                console.error("WebSocket 连接失败", err);
			                reject(err);
			            }
			        });
			
			        // 2. 监听WebSocket连接打开事件
			        uni.onSocketOpen(() => {
			            console.log("WebSocket 已打开");
						that.needContinue = true;
			
			            // 3. 发送消息
			            uni.sendSocketMessage({
			                data: JSON.stringify(data),
			                success: () => {
			                    console.log("消息发送成功");
			                },
			                fail: (err) => {
			                    console.error("消息发送失败", err);
			                }
			            });
			        });
			
			        // 4. 监听WebSocket收到消息事件（可选）
			        uni.onSocketMessage((res) => {
						console.log(res);
						that.chat = true;
						uni.hideLoading();
						let jsonData = res.data;
						let json = JSON.parse(jsonData);
						let robotMessage = json.data;
						let latestMsg = that.msgList[that.msgList.length - 1];
						
						if (!json.end) {
						    // 判断是否是思考过程
						    if (that.isThinkMode && robotMessage.indexOf("<think>") !== -1) {
						        // 开始思考 - 现在可能不需要这个条件了，因为我们预先初始化了思考区域
						        that.isThink = true;
						        robotMessage = robotMessage.replace("<think>", "");
						        if (!latestMsg.currentThinkContent) {
						            latestMsg.currentThinkContent = robotMessage;
						        } else {
						            latestMsg.currentThinkContent += robotMessage;
						        }
						        // 确保思考内容默认是展开的
						        that.$set(latestMsg, 'isThinkCollapsed', false);
						        // 滚动到底部，确保用户可以看到最新的思考内容
						        that.scrollToBottom();
						    } else if (that.isThinkMode && robotMessage.indexOf("</think>") !== -1) {
						        // 结束思考
						        that.isThink = false;
						        latestMsg.currentThinkContent += robotMessage.replace("</think>", "");
						        // 滚动到底部
						        that.scrollToBottom();
						    } else if (that.isThinkMode && that.isThink) {
						        // 深度思考过程中
						        latestMsg.currentThinkContent += robotMessage;
						        // 滚动到底部，确保用户可以看到最新的思考内容
						        that.scrollToBottom();
						    } else {
						        latestMsg.content += robotMessage;
						    }
						    console.log("机器人回复: ", robotMessage);
						} else {
						    that.chat = false;
						    that.needContinue = false;
						    that.endChatSession();
						    console.log("本轮对话已经结束.", this.chat);
						}
						resolve(res.data);
					});
			
			        // 5. 监听WebSocket关闭事件
			        uni.onSocketClose(() => {
			            console.log("WebSocket 已关闭");
						uni.hideLoading();
						that.chat = false;
			        });
			
			        // 6. 监听WebSocket错误事件
			        uni.onSocketError((err) => {
						console.log("WebSocket 连接错误");
						let latestMsg = that.msgList[that.msgList.length - 1];
						latestMsg.content = "WebSocket 连接错误";
						
						that.chat = false;
						uni.hideLoading();
			            reject(err);
			        });
			    });
			},
			endChatSession() {
			    // 关闭WebSocket连接
			    uni.closeSocket({
			        success: () => {
			            console.log("WebSocket 关闭成功");
			        },
			        fail: (err) => {
			            console.error("WebSocket 关闭失败", err);
			        }
			    });
			},
			async chatExample(that, message, url, input_type) {
			    try {
					//是否选中图片清空
					this.choosed = false;
					
					// 发送http请求
					uni.showLoading({
						title: "思考中...."
					})
					
					this.first = false;
					this.chat = true;
					
					//机器人回复新增一条记录
					let obj = {
						content: "",
						role: "robot",
						type: "string"
					}
					
					// 如果启用了思考模式，预先初始化思考内容区域
					if (this.isThinkMode) {
						obj.currentThinkContent = "";  // 初始化空的思考内容
						obj.isThinkCollapsed = false;  // 默认展开
						obj.isThink = true;            // 标记为思考模式
					}
					
					that.msgList.push(obj);
					that.scrollToBottom();
					
					let data = {};
					if (that.id > 0) {
						data = {
							"instruct": message,
							"contexts": "",
							"reset": "true",
							"dbid": that.id
						};
					} else {
						data = {
							"instruct": message,
							"contexts": "",
							"reset": "true"
						};
					}
					
					// 添加input_type参数（如果提供）
					if (input_type) {
						data.input_type = input_type;
					}
					
					// 开始聊天会话
					if (this.isThinkMode) {
						// 添加属性mode='think'
						data.mode = 'think';	
					}
			        const response = await this.startChatSession(url, data);
					console.log(response);
			    } catch (err) {
			        console.error("聊天会话出错", err);
			    }
			},
			//视觉大模型问答接口
			async versionchat(that, message) {
				// 发送http请求
				uni.showLoading({
					title: "思考中...."
				})
			
				this.first = false;
				this.chat = true;
			
				//机器人回复新增一条记录
				let obj = {
					content: "",
					role: "robot",
					type: "string"
				}
				that.msgList.push(obj);
				that.scrollToBottom();
			
				let imgBase64 = '';
				await pathToBase64(this.chattingImage).then(base64 => {
					imgBase64 = base64
				})
				
				let data = {
					"instruct": message,
					"image": imgBase64,
					"reset": "true"
				};
				const response = await this.startChatSession(url2, data);
			},
			// 发送消息
			handleSend() {
				this.chat = true;
				let message = this.chatMsg;
				this.chatMsg = ''; //清空聊天框
				let msg = {
					content: message,
					role: "human",
					type: "string"
				}
				this.msgList.push(msg);

				const that = this;
				//如果消息不为空
				if (!this.chatMsg || !/^\s+$/.test(this.chatMsg)) {
					//判断websocket接口地址，是走纯文本文档接口还是视觉问答接口
					if(this.chattingImage) {
						this.versionchat(that, message);
					} else {
						this.chatExample(that, message, url1);	// 不传input_type，默认为文本输入
					}
				} else {
					this.$modal.showToast('不能发送空白消息');
				}
			},
			// 新增思考模式切换方法
			toggleThinkMode() {
				// 关闭更多菜单
				this.showMoreMenu = false;
				
				this.isThinkMode = !this.isThinkMode;
				uni.showToast({
					title: this.isThinkMode ? '深度思考' : '标准模式',
					icon: 'none'
				});
			},
			// 添加控制更多菜单显示/隐藏的方法
			toggleMoreMenu() {
				this.showMoreMenu = !this.showMoreMenu;
			},
		}
	}
</script>
<style lang="scss" scoped>
	$chatContentbgc: #C2DCFF;
	$sendBtnbgc: #4F7DF5;

	view,
	button,
	text,
	input,
	textarea {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
	}

	.is-hover {
		color: rgba(255, 255, 255, 0.6);
		background-color: #179b16;
		border-color: #179b16;
	}

	/* 聊天消息 */
	.chat {
		.topTabbar {
			width: 100%;
			height: 90rpx;
			line-height: 90rpx;
			display: flex;
			margin-top: 80rpx;
			justify-content: space-between;

			.icon {
				margin-left: 20rpx;
			}

			.text {
				margin: auto;
				font-size: 16px;
				font-weight: 700;
			}

			.button {
				width: 10%;
				margin: auto 20rpx auto 0rpx;
			}
		}

		.scroll-view {
			::-webkit-scrollbar {
				display: none;
				width: 0 !important;
				height: 0 !important;
				-webkit-appearance: none;
				background: transparent;
				color: transparent;
			}

			background-color: #EDEDED !important; /* 微信风格的浅灰色背景 */
			background-size: cover;
			background-repeat: no-repeat;
			background-position: center center;

			.chat-body {
				display: flex;
				flex-direction: column;
				padding-top: 23rpx;

				.self {
					justify-content: flex-end;
				}

				.item {
					display: flex;
					padding: 23rpx 30rpx;

					.right {
						background-color: #95EC69 !important; /* 绿色气泡更符合微信风格 */
					}

					.left {
						background-color: #FFFFFF;
					}

					// 聊天消息的三角形
					.right::after {
						position: absolute;
						display: inline-block;
						content: '';
						width: 0;
						height: 0;
						left: 100%;
						top: 10px;
						border: 12rpx solid transparent;
						border-left: 12rpx solid #95EC69 !important;
					}

					.left::after {
						position: absolute;
						display: inline-block;
						content: '';
						width: 0;
						height: 0;
						top: 10px;
						right: 100%;
						border: 12rpx solid transparent;
						border-right: 12rpx solid #FFFFFF;
					}

					.content {
						position: relative;
						max-width: 486rpx;
						border-radius: 8rpx;
						word-wrap: break-word;
						padding: 24rpx 24rpx;
						margin: 0 24rpx;
						border-radius: 5px;
						font-size: 30rpx;
						font-family: PingFang SC;
						font-weight: 300;
						color: #000000;
						opacity: 0.85;
						line-height: 42rpx;
						
						/* 思考内容样式 */
						&.think-mode {
							background-color: #f0f4f8;
						}
					}

					.avatar {
						display: flex;
						justify-content: center;
						width: 60rpx;
						height: 60rpx;
						background: $sendBtnbgc;
						border-radius: 50rpx;
						overflow: hidden;

						image {
							align-self: center;
						}
					}
				}
			}
		}

		/* 底部聊天发送栏 */
		.chat-bottom {
			width: 100%;
			min-height: 100rpx;
			background-color: #F5F5F5;
			transition: all 0.1s ease;
			display: flex; /* 新增 */
			align-items: center; /* 新增 */
			justify-content: center; /* 新增 */
			position: relative; /* 新增 */

			.send-msg {
				display: flex;
				align-items: flex-end; /* 修改: 从center改为flex-end，使元素底对齐 */
				padding: 16rpx 30rpx;
				width: 100%;
				min-height: 120rpx;
				position: relative; /* 修改: 从fixed改为relative */
				transition: all 0.1s ease;
				
				/* 操作按钮样式 */
				.action-btn {
					width: 60rpx;
					height: 60rpx;
					margin: 0 10rpx;
					margin-bottom: 8rpx; /* 新增: 添加底部外边距，对齐文本框底部 */
					border-radius: 50%;
					border: 2px solid #e0e0e0;
					background-color: transparent !important;
					color: rgba(0,0,0,0.9);
					padding: 0;
					display: flex;
					align-items: center;
					justify-content: center;
					align-self: flex-end; /* 新增: 将按钮自身对齐到flex容器底部 */
				}
				
				.action-btn button {
					background-color: #FFFFFF !important;
					// color: rgba(0,0,0,0.9);
					border: 2px solid #e0e0e0;
					border-radius: 50%;
					font-size: 36rpx;
					width: 60rpx;
					height: 60rpx;
					line-height: 60rpx;
					font-weight: normal;
					display: flex;
					align-items: center;
					justify-content: center;
				}
				
				.iconfont {
					font-size: 36rpx;
					display: flex;
					align-items: center;
					justify-content: center;
				}
				
				/* 更多按钮样式 */
				.more-btn {
					position: relative;
					
					.more-icon {
						font-size: 40rpx;
						font-weight: normal;
						color: #7F7F7F;
					}
				}
				
				/* 清空按钮图标样式 */
				.clear-icon {
					font-size: 28rpx;
					color: #7F7F7F;
				}
				
				/* 输入框样式 */
				.uni-textarea {
					flex: 1;
					padding-bottom: 0;
					margin: 0 10rpx;
					display: flex; /* 新增: 设为flex布局 */
					align-items: flex-start; /* 修改: 从center改为flex-start，允许文本域向上扩展 */
					
					textarea {
						width: 100%;
						min-height: 45rpx;
						height: auto; /* 修改: 改为自动高度，允许根据内容扩展 */
						max-height: 600rpx; /* 修改: 设置最大高度限制 */
						background: #FFFFFF;
						border-radius: 10rpx;
						font-size: 28rpx;
						font-weight: normal;
						font-family: PingFang SC;
						color: #333333;
						line-height: 45rpx; /* 修改: 恢复正常行高 */
						padding: 16rpx; /* 修改: 恢复正常内边距 */
						text-indent: 0;
						box-sizing: border-box;
						overflow-y: auto;
					}
					
					/* 语音按钮样式 */
					button {
						background-color: #FFFFFF !important;
						color: #333333;
						border: none;
						width: 100% !important;
						height: 75rpx !important;
						line-height: 75rpx !important;
						font-size: 30rpx;
						font-weight: normal;
						border-radius: 10rpx;
					}
				}
				
				/* 发送按钮样式 */
				.send-btn {
					display: flex;
					align-items: center;
					justify-content: center;
					margin-left: 10rpx;
					width: 200rpx;
					height: 65rpx;
					background: #007CFE;
					border-radius: 10rpx;
					font-size: 30rpx;
					font-family: PingFang SC;
					font-weight: 500;
					color: #FFFFFF;
					line-height: 28rpx;
					align-self: flex-end; /* 新增: 确保发送按钮在底部对齐 */
					margin-bottom: 6rpx; /* 新增: 调整底部边距以对齐 */
				}
			}
			
			/* 更多菜单样式 */
			.more-menu-container {
				position: absolute;
				left: 0;
				right: 0;
				bottom: 100%;  /* 修改: 从180rpx改为100%，使其位于send-msg上方 */
				background-color: #f5f5f5;  /* 修改: 从半透明改为与底部栏一致的背景色f5f5f5 */
				z-index: 999;
				animation: slide-up 0.3s ease;
				border-top: 1px solid #e0e0e0; 
				border-top-left-radius: 15rpx;
				border-top-right-radius: 15rpx;
				box-shadow: 0 1px 5px rgba(0,0,0,0.1); /* 新增: 添加阴影效果增强分隔感 */
			}
			
			.more-menu {
				background-color: #f5f5f5;  /* 修改: 与底部栏背景色一致 */
				padding: 10rpx 20rpx; /* 减小内边距，降低整体高度 */
				display: flex;
				flex-wrap: wrap;
				border-top-left-radius: 15rpx;
				border-top-right-radius: 15rpx;
				position: relative;  /* 新增: 为添加底部分隔线做准备 */
			}
			
			.more-menu::after {  /* 新增: 添加底部分隔线 */
				content: '';
				position: absolute;
				left: 20rpx;
				right: 20rpx;
				bottom: 0;
				height: 1px;
				background-color: #e0e0e0;
			}

			.menu-item {
				width: 120rpx; /* 减小宽度从20%到18% */
				height: 120rpx; /* 减小高度从20%到18% */
				display: flex;
				flex-direction: column;
				align-items: center;
				padding: 10rpx 0; /* 减小内边距从15rpx到10rpx，降低高度 */
				background-color: #fff;
				border-radius: 8rpx; /* 略微减小圆角 */
				margin-left: 6rpx; /* 略微减小外边距 */
				margin-right:20rpx;
				box-shadow: 0 1px 2px rgba(0,0,0,0.06); /* 减轻阴影 */
				
				.menu-icon {
					font-size: 50rpx; /* 减小图标大小从60rpx到50rpx */
					margin-bottom: 6rpx; /* 减小底部间距 */
					
					&.active-mode {
						color: #4CAF50;
					}
				}
				
				text {
					font-size: 22rpx; /* 减小文本大小从24rpx到22rpx */
					color: #666;
				}
			}
		}
	}

	.record-container {
		width: 100% !important;
		height: 100% !important;
		background-color: rgba(255, 255, 255, 0.8);
		position: absolute;
		left: 0;
		right: 0;
		top: 0;
		bottom: 0;
		margin: auto;
		box-sizing: border-box;
		border-radius: 30rpx;
		z-Index: 9999;
		display: flex !important;
		align-items: center !important;
		flex-direction: column;
		justify-content: center;

		.record-logo {
			background-color: lawngreen;
			width: 250rpx;
			height: 100rpx;
			border-radius: 10rpx;
			text-align: center;
			line-height: 100rpx;
		}
	}

	.message-container {
		display: flex;
		flex-direction: column;
		background-color: #FFFFFF;
		max-width: 400rpx;
		border-radius: 10rpx;
	}

	.message {
		background-color: #FFFFFF;
		width: 80rpx;
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-radius: 10rpx;
		margin-right: 10rpx;
	}

	.voice-img {
		margin-right: 10rpx;
		width: 50rpx;
		height: 50rpx;
		transform: rotate(180deg);
	}

	/* 弹出层默认样式 */
	.Popup {
		width: 100%;
		height: 100%;
		background: #FFFFFF;
		position: absolute;
		left: 0;
		top: 0;
		z-index: 9;
		transition: all 0.25s linear;
	}

	.chat-custom-right {
		flex: 1;
		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */
		flex-direction: column;
		justify-content: space-between;
		align-items: flex-end;
	}

	.chat-custom-text {
		font-size: 12px;
		color: #999;
	}

	/* 思考容器样式 */
	.think-container {
		margin-bottom: 10rpx;
		border-left: 4rpx solid #4CAF50;
		padding-left: 10rpx;
		background-color: #f8f8f8;
		border-radius: 6rpx;
		overflow: hidden;
	}

	/* 思考标题栏样式 */
	.think-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 8rpx 10rpx;
		background-color: rgba(76, 175, 80, 0.1);
		cursor: pointer;
	}

	/* 思考标签样式 */
	.think-label {
		font-size: 24rpx;
		color: #4CAF50;
		font-weight: bold;
	}

	/* 折叠图标样式 */
	.think-collapse-icon {
		font-size: 24rpx;
		color: #666;
		background-color: #e0e0e0;
		padding: 2rpx 8rpx;
		border-radius: 4rpx;
	}

	/* 思考内容样式 */
	.think-content {
		padding: 10rpx;
		font-size: 28rpx;
		color: #666;
		background-color: rgba(76, 175, 80, 0.05);
		border-top: 1px dashed #e0e0e0;
		max-height: 600rpx;
		overflow-y: auto;
	}
	
	/* 思考中指示器样式 */
	.thinking-indicator {
		color: #4CAF50;
		animation: pulsate 1.5s infinite;
	}

	/* 思考中的光标样式 */
	.thinking-cursor {
		display: inline-block;
		width: 4rpx;
		height: 24rpx;
		background-color: #4CAF50;
		animation: blink 0.8s infinite;
		margin-left: 4rpx;
		vertical-align: middle;
	}

	@keyframes pulsate {
		0% { opacity: 1; }
		50% { opacity: 0.5; }
		100% { opacity: 1; }
	}

	@keyframes blink {
		0% { opacity: 0; }
		49% { opacity: 0; }
		50% { opacity: 1; }
		100% { opacity: 1; }
	}
	
	@keyframes slide-up {
		from { transform: translateY(100%); }
		to { transform: translateY(0); }
	}
	
	/* 附件图片样式 */
	.atta-image {
		display: flex;
		justify-content: space-between;
		background-color: #E8E8E8;
		border-radius: 5rpx;
		padding: 0 10rpx;
		
		div {
			height: 10rpx;
			line-height: 10rpx;	
			font-size: 12rpx;
		}
		.atta-image-close {
			cursor: pointer;
			font-weight: normal;
		}
	}
</style>

<style>
	.animation-class {
		animation: fade-in 1s;
	}

	@keyframes fade-in {
		0% {
			opacity: 0;
		}

		100% {
			opacity: 1;
		}
	}
</style>

<style lang="scss">
	.slot-box {
		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */
		flex-direction: row;
		align-items: center;
	}

	.slot-image {
		/* #ifndef APP-NVUE */
		display: block;
		/* #endif */
		margin-right: 10px;
		width: 30px;
		height: 30px;
	}

	.slot-text {
		flex: 1;
		font-size: 14px;
		color: #4cd964;
		margin-right: 10px;
	}

	.btn-class {
		margin-left: 10rpx !important;
		width: 70rpx !important;
	}
</style>