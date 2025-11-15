<template>
	<view>
		<view class="page-body">
			<view class="page-section page-section-gap" style="text-align: center;">
				<audio style="text-align: left" :src="current.src" :poster="current.poster" :name="current.name"
					:author="current.author" :action="audioAction" controls></audio>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				current: {
					poster: 'https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/music-a.png',
					name: '致爱丽丝',
					author: '暂无',
					src: 'https://web-ext-storage.dcloud.net.cn/uni-app/ForElise.mp3',
				},
				audioAction: {
					method: 'pause'
				}
			}
		}
	}
</script>

<style>

</style>