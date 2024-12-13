<template>
	<div id="father">
		<n-divider>
			<img src="https://s1.imagehub.cc/images/2024/12/10/3a2621aff049cdd9a933496dbf93d930.png" id="avatar">
		</n-divider>
		<n-highlight style="margin-bottom: 5px;" :text="headText" :patterns="patterns" :highlight-style="{
			padding: '0 6px',
			margin: '0 6px',
			borderRadius: themeVars.borderRadius,
			display: 'inline-block',
			color: 'black',
			background: 'Pink',
			transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
		}" />
		<n-highlight :text="text" :patterns="patterns" :highlight-style="{
			padding: '0 6px',
			margin: '0 6px',
			borderRadius: themeVars.borderRadius,
			display: 'inline-block',
			color: 'black',
			background: 'Pink',
			transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
		}" />
		<n-divider>
			<n-gradient-text type="info" :size="25">
				向我提意见
			</n-gradient-text>
		</n-divider>
		<n-tooltip trigger="hover" placement="bottom">
			<template #trigger>
				<n-float-button position="relative"
					@click="blankClick('https://github.com/windhide/SkyMusicPlay-for-Windows/pulls')">
					<n-icon>
						<GitPullRequest />
					</n-icon>
				</n-float-button>
			</template>
			有更好的功能？来提Request！
		</n-tooltip>
		<n-tooltip trigger="hover" placement="bottom">
			<template #trigger>
				<n-float-button position="relative" style="margin: 0 30px;"
					@click="blankClick('https://github.com/windhide/SkyMusicPlay-for-Windows')">
					<n-icon>
						<LogoGithub />
					</n-icon>
				</n-float-button>
			</template>
			点个星星吧靓仔
		</n-tooltip>
		<n-tooltip trigger="hover" placement="bottom">
			<template #trigger>
				<n-float-button position="relative"
					@click="blankClick('https://github.com/windhide/SkyMusicPlay-for-Windows/issues/new')">
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
import { useThemeVars } from 'naive-ui'
import { GitPullRequest, LogoGithub, Build } from '@vicons/ionicons5'
import { sendData, getData, getWWWData } from '@/utils/fetchUtils'
import router from '@/router';
import { useDialog  } from 'naive-ui'

const themeVars = useThemeVars()
let headText = '如果您觉得好用可以赏我一杯咖啡☕'
let text = '欢迎使用本软件，本软件完全免费，如果您是买的本软件就是被骗了'
let patterns = ['完全免费', '被骗了', '咖啡☕']
const dialog = useDialog()

function blankClick(url) {
	getData("openBrowser?url=" + url)
}

function jump() {
	if (window.innerWidth > 700) {
		// 更新检测
		getWWWData("https://raw.githubusercontent.com/windhide/SkyMusicPlay-for-Windows/main/.version").then(res => {
			let updateMesseage = JSON.parse(res)
			if (updateMesseage.version > require('./../../package.json').version) {
				dialog.success({
					title: updateMesseage.title,
					content: updateMesseage.content,
					positiveText: updateMesseage.positiveText,
					contentStyle: { whiteSpace: 'pre-wrap' },
					maskClosable: false
				})
			}
		})
		return
	}
	sendData("nextSheet", { type: '不ok' }).then(res => {
		if (res.length != 0)
			router.push({ name: "keyboard" })
	})
}
jump()
</script>

<style scoped>
#father {
	display: flex;
	justify-content: center;
	align-items: center;
	flex-wrap: wrap
}

#avatar {
	height: 250px;
	width: 250px;
}
</style>