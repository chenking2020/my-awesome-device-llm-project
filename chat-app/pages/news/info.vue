<template>
	<view>
		<rich-text :nodes="strings"></rich-text>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				id:"",
				content:"",
				nodes: [{
					name: 'div',
					attrs: {
						class: 'div-class',
						style: 'line-height: 60px; color: red; text-align:center;'
					},
					children: [{
						type: 'text',
						text: 'Hello&nbsp;uni-app!'
					}]
				}],				
				strings: ''
			}
		},
		onLoad(options) {
			this.getDetail(options.id);
		},
		methods: {
			getDetail(id) {
				uni.request({
					url:"https://unidemo.dcloud.net.cn/api/news/36kr/"+id,
					method:"GET",
					data:{},
					success: res => {
						this.strings = res.data.content;
					},
					fail: () => {}
				})
				
			}
		}
	}
</script>

<style>

</style>
