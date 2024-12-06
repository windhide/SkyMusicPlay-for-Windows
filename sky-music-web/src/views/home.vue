<template>
	<div id="father">
		<n-divider>
				<img src="https://s1.imagehub.cc/images/2024/12/02/751628702b15b19942a74f79c58117c2.png" id="avatar">
		</n-divider>
		<n-highlight :text="text" :patterns="patterns" :highlight-style="{
			padding: '0 6px',
			borderRadius: themeVars.borderRadius,
			display: 'inline-block',
			color: themeVars.baseColor,
			background: themeVars.primaryColor,
			transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
		}" />
		<n-divider>
			<n-gradient-text type="info" :size="25">
				向我提意见
			</n-gradient-text>
		</n-divider>
		<n-tooltip trigger="hover" placement="bottom">
			<template #trigger>
				<n-float-button position="relative" @click="blankClick('https://github.com/windhide/SkyMusicPlay-for-Windows/pulls')" >
					<n-icon>
						<GitPullRequest />
					</n-icon>
				</n-float-button>
			</template>
			有更好的功能？来提Request！
		</n-tooltip>
		<n-tooltip trigger="hover" placement="bottom">
			<template #trigger>
				<n-float-button position="relative" style="margin: 0 30px;"  @click="blankClick('https://github.com/windhide/SkyMusicPlay-for-Windows')" >
					<n-icon>
						<LogoGithub />
					</n-icon>
				</n-float-button>
			</template>
			点个星星吧靓仔
		</n-tooltip>
		<n-tooltip trigger="hover" placement="bottom">
			<template #trigger>
				<n-float-button position="relative" @click="blankClick('https://github.com/windhide/SkyMusicPlay-for-Windows/issues/new')">
					<n-icon>
						<Build />
					</n-icon>
				</n-float-button>
			</template>
			向我提功能需求或者提bug！
		</n-tooltip>
	</div>
</template>

<script setup lang="ts">
import { useMessage, useThemeVars } from 'naive-ui'
import { GitPullRequest, LogoGithub, Build } from '@vicons/ionicons5'
const message = useMessage()

const themeVars = useThemeVars()
let text = '欢迎使用本软件，本软件完全免费，如果您是买的本软件就是被骗了'
let patterns = ['完全免费', '被骗了']
function blankClick(url){
	navigator.clipboard.writeText(url); // 使用Clipboard API复制内容
	message.success("请复制到浏览器打开啦~！")
}
</script>

<style scoped>
#father {
	display: flex;
	justify-content: center;
	align-items: center;
	flex-wrap: wrap
}

#avatar {
	height: 150px;
	width: 150px;
}
</style>