<template>
    <el-row class="tac">
        <el-col>
            <el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-menu-vertical-demo"
                :default-active="$route.path" text-color="#fff">
                <el-menu-item index="/mainBoard/diagnosis" @click="changeActive('/mainBoard/diagnosis')">
                    <el-icon>
                        <Search />
                    </el-icon>
                    <span>诊断</span>
                </el-menu-item>

                <el-menu-item index="/mainBoard/analyze" @click="changeActive('/mainBoard/analyze')">
                    <el-icon>
                        <ChatLineSquare />
                    </el-icon>
                    <span>结果分析</span>
                </el-menu-item>

                <el-menu-item index="/mainBoard/encipher" @click="changeActive('/mainBoard/encipher')">
                    <el-icon>
                        <Lock />
                    </el-icon>
                    <span>加密</span>
                </el-menu-item>


                <el-menu-item index="/mainBoard/decrypt" @click="changeActive('/mainBoard/decrypt')">
                    <el-icon>
                        <Unlock />
                    </el-icon>
                    <span>解密</span>
                </el-menu-item>


                <el-menu-item index="/mainBoard/security" @click="changeActive('/mainBoard/security')">
                    <el-icon>
                        <Aim />
                    </el-icon>
                    <span>安全性分析</span>
                </el-menu-item>

                <el-menu-item index="/mainBoard/setting" @click="changeActive('/mainBoard/setting')">
                    <el-icon>
                        <setting />
                    </el-icon>
                    <span>设置</span>
                </el-menu-item>
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

import { useRoute, useRouter } from 'vue-router';
let $route = useRoute();
let $router = useRouter();


//如果有参数的话，可以使用query
const changeActive = (path: string) => {
    $router.push({ path, query: {} })
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