<template>
    <div class="diagnosis">
        <input type="file" ref="fileInput" @change="onFileChange" style="display: none;" multiple />
        <div class="images-container">
            <div class="image-wrapper">
                <img v-show="beforeEncipher !== ''" :src="beforeEncipher" alt="Uploaded Image" />
                <button v-show="beforeEncipher !== ''" @click="openImage(beforeEncipher)">打开图片</button>
            </div>
            <div class="image-wrapper">
                <img v-show="EncipherImageUrl !== null" :src="EncipherImageUrl" alt="检测结果图像" class="post-diagnosis" />
                <button v-show="EncipherImageUrl !== null" @click="openImage(EncipherImageUrl)">打开图片</button>
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
</template>

<script setup lang='ts'>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const beforeEncipher = ref<string>('');
const fileInput = ref<HTMLInputElement | null>(null);
const EncipherImageUrl = ref<string | null>(null);
const isLoading = ref<boolean>(false);

const onFileChange = async (event: Event) => {
    const files = (event.target as HTMLInputElement).files;
    if (files && files.length > 0) {
        isLoading.value = true; // 开始加载

        // 将文件转换为 URL 并存储
        const file = files[0];
        // imageUrls.value = URL.createObjectURL(file);

        // 上传图片并保存到服务器
        const formData = new FormData();
        formData.append('file', file, 'pt.jpg');
        await axios.post('/upload', formData);

        // 运行 Python 脚本
        await axios.post('/run-script');

        //这里是因为上传的图片会重命名为pt.jpg保存在/input下
        beforeEncipher.value = '/input/pt.jpg'
        localStorage.setItem('beforeEncipher', beforeEncipher.value);

        // 更新右侧的图片
        EncipherImageUrl.value = '/output/jiami.jpg';
        localStorage.setItem('EncipherImageUrl', EncipherImageUrl.value);

        window.location.reload(); // 刷新页面
    }
};

const triggerFileUpload = () => {
    fileInput.value?.click();
};

const openImage = (url: string | null) => {
    if (url) {
        window.open(url, '_blank');
    }
};

onMounted(() => {
    // 从本地存储加载图片 URL
    const storedImageUrls = localStorage.getItem('beforeEncipher');
    if (storedImageUrls) {
        beforeEncipher.value = storedImageUrls;
    }

    const storedEncipherImageUrl = localStorage.getItem('EncipherImageUrl');
    if (storedEncipherImageUrl) {
        EncipherImageUrl.value = storedEncipherImageUrl;
    }
});
</script>

<style lang="scss" scoped>
.diagnosis {
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