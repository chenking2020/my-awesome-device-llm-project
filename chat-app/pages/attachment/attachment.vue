<template>
	<view class="container">
		<uni-section :title="title" type="line">
			<uni-list>
				<uni-list-item :title="item.filename" :note="item.filepath" showArrow
					thumb="https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png" thumb-size="base"
					v-for="(item,index) in attaList" :key="index" />
			</uni-list>
		</uni-section>
		<button type="primary" size="default" @click="goback">返回</button>
	</view>
</template>

<script>
	export default {
		name:"attachment",
		components: {},
		data() {
			return {
				title: "显示图标或图片下的附件",
				id:0,
				attaList:[]
			};
		},
		onLaunch: function(options) {
			console.log('App Launch')
		},
		onLoad(option) {
			this.id = option.id;
			this.title = option.name;
			this.getList();
		},
		onBackPress() {
			console.log('onBackPress');
		},
		methods: {
			//获取数据列表
			getList() {
				uni.showLoading({
					title: '数据请求中'
				})

				const url = "http://39.105.215.32/chatmt/v1/kbs_reldocs";
				uni.request({
					url: url,
					data: {
						id: this.id
					},
					success: (res) => {
						let data = res.data;
						this.attaList = data.data;
						uni.hideLoading();
					},
					fail: (res) => {
						uni.hideLoading();
					}
				});
			},
			goback(e) {
				uni.navigateTo({
					url: '/pages/index/index?showFile=true'
				});
			}
		}
	};
</script>

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
</style>