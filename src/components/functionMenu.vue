<template>
    <el-row class="tac">
        <el-col>
            <el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-menu-vertical-demo"
                default-active="2" text-color="#fff" @open="handleOpen" @close="handleClose">


                <router-link to="/diagnosis">
                    <el-menu-item index="1">
                        <el-icon>
                            <Search />
                        </el-icon>
                        <span>诊断</span>
                    </el-menu-item>
                </router-link>

                <router-link to="/analyze">
                    <el-menu-item index="2">
                        <el-icon>
                            <ChatLineSquare />
                        </el-icon>
                        <span>结果分析</span>
                    </el-menu-item>
                </router-link>

                <router-link to="/encipher">
                    <el-menu-item index="3">
                        <el-icon>
                            <Lock />
                        </el-icon>
                        <span>加密</span>
                    </el-menu-item>
                </router-link>

                <router-link to="/decrypt">
                    <el-menu-item index="4">
                        <el-icon>
                            <Unlock />
                        </el-icon>
                        <span>解密</span>
                    </el-menu-item>
                </router-link>

                <router-link to="/security">
                    <el-menu-item index="5">
                        <el-icon>
                            <Aim />
                        </el-icon>
                        <span>安全性分析</span>
                    </el-menu-item>
                </router-link>

                <router-link to="/setting">
                    <el-menu-item index="6">
                        <el-icon>
                            <setting />
                        </el-icon>
                        <span>设置</span>
                    </el-menu-item>
                </router-link>
            </el-menu>
        </el-col>
    </el-row>
</template>

<script lang="ts" setup>
import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
} from '@element-plus/icons-vue'
const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
</script>

<style lang="scss">
.el-menu-vertical-demo {

    height: 100vh;

    .el-menu-item {
        height: 10vh;
        line-height: 10vh;
        font-size: 2vh;
    }
}
</style>