<script>
	export default {
		onLaunch: function() {
			console.log('App 启动');
		},
		onShow: function() {
			console.log('App 展示');
		},
		onHide: function() {
			console.log('App 隐藏');
		}
	}
</script>

<style>
	/*每个页面公共css */
	@import "./common/uni.css"
	
	page, view {
		display: flex;
	}
</style>
