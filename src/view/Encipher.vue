<template>
    <div class="encipher">
        <input type="file" ref="fileInput" @change="onFileChange" style="display: none;" multiple />
        <div class="images-container">
            <div class="image-wrapper">
                <img v-show="encipherStore.leftImg !== ''" :src="encipherStore.leftImg" alt="" />
                <button v-show="encipherStore.leftImg !== ''" @click="openImage(encipherStore.leftImg)">打开图片</button>
            </div>
            <div class="image-wrapper">
                <img v-show="encipherStore.rightImg !== ''" :src="encipherStore.rightImg" alt=""
                    class="post-encipher" />
                <button v-show="encipherStore.rightImg !== ''" @click="openImage(encipherStore.rightImg)">打开图片</button>
            </div>
        </div>
        <div class="eventButton">
            <button class="upload-button" @click="triggerFileUpload">选择图像</button>
        </div>
        <div v-if="isLoading" class="loading-overlay">
            <div class="spinner"></div>
            <p>正在处理，请稍候...</p>
        </div>
    </div>
    <MyDialog />
</template>

<script setup lang='ts'>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import useDialogStore from '../store/dialog';
import MyDialog from '../components/myDialog.vue';
import useEncipherStore from '../store/encipher';
import useSecurityStore from '../store/security';
const encipherStore = useEncipherStore();
const DialogStore = useDialogStore();
const securityStore = useSecurityStore();

const fileInput = ref<HTMLInputElement | null>(null);
const isLoading = ref<boolean>(false);


const onFileChange = async (event: Event) => {
    const files = (event.target as HTMLInputElement).files;
    if (files && files.length > 0) {
        // 显示对话框并等待关闭
        encipherStore.leftImg = '';
        encipherStore.rightImg = '';
        await showDialogAndWait();
        isLoading.value = true; // 开始加载

        const file = files[0];

        // 上传图片并保存到服务器
        const formData = new FormData();
        formData.append('file', file, 'pt2.bmp');
        await axios.post('/upload-encipher', formData);

        // 运行 Python 脚本
        await axios.post('/run-script-en');
        await axios.post('/run-script-chart');

        const timestamp = new Date().getTime();
        securityStore.leftImg = `../../output/histogram.jpg?timestamp=${timestamp}`;
        securityStore.rightImg = `../../output/histogram2.jpg?timestamp=${timestamp}`;

        encipherStore.leftImg = `/input/pt2.bmp?timestamp=${timestamp}`;

        // 更新右侧的图片
        encipherStore.rightImg = `/output/jiami.bmp?timestamp=${timestamp}`;

        isLoading.value = false;

    }
};

import { watch } from 'vue';

const showDialogAndWait = () => {
    return new Promise<void>((resolve) => {
        DialogStore.visiable = true;
        const unwatch = watch(() => DialogStore.visiable, (newVal) => {
            if (!newVal) {
                unwatch();
                resolve();
            }
        });
    });
};

const triggerFileUpload = () => {
    fileInput.value?.click();
};

const openImage = (url: string | null) => {
    if (url) {
        window.open(url, '_blank');
    }
};

</script>

<style lang="scss" scoped>
.encipher {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    .images-container {
        width: 100%;
        height: 85%;
        display: flex;
        justify-content: space-around;

        .image-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;

            img {
                max-width: 90%;
                max-height: 90%;
                min-height: 90%;
                min-width: 90%;
                object-fit: contain;
            }

            button {
                margin-top: 10px;
                padding: 15px 85px;
                // background-color: skyblue;
                background-color: rgb(84, 92, 100);
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            button:hover {
                background-color: green;
                color: white;
            }
        }
    }

    .eventButton {
        padding: 1%;
        height: 15%;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;

        .upload-button {
            margin-top: 7vh;
            width: 25%;
            // background-color: skyblue;
            background-color: rgb(84, 92, 100);
            color: white;
            cursor: pointer;
            border-radius: 5px;
            position: absolute;
            font-size: 3vh;
        }

        .upload-button:hover {
            color: white;
            background-color: green;
        }
    }

    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        color: white;
    }

    .spinner {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 4px solid white;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }

        100% {
            transform: rotate(360deg);
        }
    }
}
</style>