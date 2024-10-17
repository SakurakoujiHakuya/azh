<template>
    <div class="diagnosis">
        <input type="file" ref="fileInput" @change="onFileChange" style="display: none;" multiple />
        <div class="images-container">
            <div class="image-wrapper">
                <img v-show="imageUrls !== ''" :src="imageUrls" alt="Uploaded Image" />
                <button v-show="imageUrls !== ''" @click="openImage(imageUrls)">打开图片</button>
            </div>
            <div class="image-wrapper">
                <img v-show="diagnosisImageUrl !== null" :src="diagnosisImageUrl" alt="检测结果图像" class="post-diagnosis" />
                <button v-show="diagnosisImageUrl !== null" @click="openImage(diagnosisImageUrl)">打开图片</button>
            </div>
        </div>
        <div class="eventButton">
            <button class="upload-button" @click="triggerFileUpload">选择图像</button>
        </div>
    </div>
</template>

<script setup lang='ts'>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const imageUrls = ref<string>(localStorage.getItem('imageUrls') || '');
const fileInput = ref<HTMLInputElement | null>(null);
const diagnosisImageUrl = ref<string | null>(localStorage.getItem('diagnosisImageUrl'));

const onFileChange = async (event: Event) => {
    const files = (event.target as HTMLInputElement).files;
    if (files && files.length > 0) {
        // 将文件转换为 URL 并存储
        const file = files[0];
        imageUrls.value = URL.createObjectURL(file);
        localStorage.setItem('imageUrls', imageUrls.value);

        // 上传图片并保存到服务器
        const formData = new FormData();
        formData.append('file', file, 'pt.jpg');
        await axios.post('/upload', formData);

        // 运行 Python 脚本
        await axios.post('/run-script');

        // 更新右侧的图片
        diagnosisImageUrl.value = '/output/feature_map_layer_0.png';
        localStorage.setItem('diagnosisImageUrl', diagnosisImageUrl.value);
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
    const storedImageUrls = localStorage.getItem('imageUrls');
    if (storedImageUrls) {
        imageUrls.value = storedImageUrls;
    }

    const storedDiagnosisImageUrl = localStorage.getItem('diagnosisImageUrl');
    if (storedDiagnosisImageUrl) {
        diagnosisImageUrl.value = storedDiagnosisImageUrl;
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
                padding: 5px 10px;
                background-color: skyblue;
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
            background-color: skyblue;
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
}
</style>