<template>

    <el-dialog v-model="DialogStore.visiable" title="密钥" width="500" align-center>
        <template #footer>
            <div class="dialog-footer">
                <el-input v-model="key" placeholder="请输入密钥" class="keyInput"></el-input>
                <el-button @click="DialogStore.visiable = false">取消</el-button>
                <el-button type="primary" @click="inputK">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const key = ref<string>('')
import useDialogStore from '../store/dialog';
const DialogStore = useDialogStore();
const inputK = () => {
    DialogStore.inputKey = key.value
    DialogStore.visiable = false
    console.log(DialogStore.inputKey)
}
</script>
<style>
.keyInput {
    margin-bottom: 30px;
}
</style>