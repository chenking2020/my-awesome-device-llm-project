<template>
	<view class="bg">
		<view class="openBox" v-if="!isOpen">
			<view @tap="next(0)">开始</view>
		</view>
		<view class="stepBox">
			<video :src="videoList[step].url" id="myVideo" :controls='false' :show-fullscreen-btn='false' autoplay
				@ended="showbtn" :show-play-btn='false' :show-center-play-btn='false' :show-loading='false'
				:enable-progress-gesture='false' object-fit='cover'></video>
			<view class="infoBox">
				<view class="skip" @tap="skip">跳过</view>
				<view class="btns" v-if="isShowbtn">
					<view @tap="next(i.step)" :style="{animation:`show ${(index+2)*0.2}s`}"
						v-for="(i,index) in videoList[step].btnList">
						{{i.info}}
					</view>
				</view>
			</view>
		</view>
	</view>
</template>
<script>
	export default {
		data() {
			return {
				isOpen: false,
				videoObj: null,
				step: 0,
				isShowbtn: false,
				videoList: [{
						url: '../../static/video/custom_service.mp4',
						btnList: [{
								step: 0,
								info: '重新播放'
							}, {
								step: 1,
								info: '吃饭'
							},
							{
								step: 2,
								info: '喝水'
							},
						]
					},
					{
						url: '../../static/video/--0xL_wWq_0.9_2.mp4',
						btnList: [{
								step: 1,
								info: '重新播放'
							},
							{
								step: 0,
								info: '工作'
							},
							{
								step: 2,
								info: '喝水'
							},
						]
					},
					{
						url: '../../static/video/--0xL_wWq_0.9_3.mp4',
						btnList: [{
								step: 2,
								info: '重新播放'
							},
							{
								step: 0,
								info: '工作'
							},
							{
								step: 1,
								info: '吃饭'
							},
						]
					}
				]
			}
		},
		onLoad() {

		},
		onReady() {
			this.videoObj = uni.createVideoContext('myVideo')
		},
		methods: {
			skip() {
				this.videoObj.seek(999999999999)
			},
			replay() {
				this.isShowbtn = false
				this.videoObj.seek(0)
				this.videoObj.play()
			},
			next(step) {
				this.isOpen = true
				this.isShowbtn = false
				this.step = step
				this.videoObj.seek(0)
				this.videoObj.play()
			},
			showbtn() {
				this.isShowbtn = true
			},

		}
	}
</script>

<style lang="scss" scoped>
	.bg {
		background-color: #000;
		position: fixed;
		width: 100%;
		height: 100%;

		.openBox {
			position: absolute;
			top: 0;
			left: 0;
			z-index: 99;
			width: 100%;
			height: 100%;
			background-color: rgba(0, 0, 0, 0.8);
			display: flex;
			justify-content: center;
			align-items: center;

			view {
				background-color: #007AFF;
				color: #FFFFFF;
				border-radius: 100rpx;
				padding: 15rpx 300rpx;
				transition: 0.2s;
				font-size: 56px;
				font-weight: bold;
				transition: 0.2s;

				&:hover {
					transform: scale(1.1);
				}

				&:active {
					transform: scale(0.9);
				}
			}
		}

		.stepBox {
			width: 100%;
			height: 100%;
			position: relative;

			.infoBox {
				position: absolute;
				width: 100%;
				height: 100%;
				top: 0;
				left: 0;
				// background-color: rgba(0,0,0,0.5);
				display: flex;
				flex-direction: column;
				justify-content: flex-end;

				.skip {
					position: absolute;
					top: 80rpx;
					right: 80rpx;
					background-color: #007AFF;
					color: #FFFFFF;
					border-radius: 60rpx;
					padding: 15rpx 60rpx;
					transition: 0.2s;
					font-size: 22px;
					font-weight: bold;

					&:hover {
						transform: scale(1.1);
					}

					&:active {
						transform: scale(0.9);
					}
				}

				.btns {
					padding: 200rpx 30rpx;
					width: 600rpx;
					animation: opacityShow 0.2s;

					view {
						text-align: center;
						margin-bottom: 30rpx;
						padding: 30rpx;
						border-top: 5rpx solid #333;
						border-bottom: 5rpx solid #333;
						transition: 0.2s;

						&:hover {
							background-color: rgba(0, 0, 0, 0.1);
							transform: scale(0.95);
						}

						&:active {
							background-color: rgba(0, 0, 0, 0.1);
							transform: scale(0.9);
						}
					}
				}
			}

			video {
				width: 100%;
				height: 100%;
			}

		}
	}
</style>