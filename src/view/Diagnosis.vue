<template>
    <div class="diagnosis">
        <input type="file" ref="fileInput" @change="onFileChange" style="display: none;" multiple />
        <div class="images-container">
            <div class="image-wrapper">
                <img v-show="imageUrls.length > 0" :src="imageUrls[currentIndex]" alt="Uploaded Image" />
                <!-- <img v-show="imageUrls.length > 0" :src="imageUrls[currentIndex]" alt="Uploaded Image"
                    v-if="DiagnosisStore.orignImg === ''" /> -->
                <!-- <img :src="DiagnosisStore.orignImg" alt="Uploaded Image" v-else /> -->
            </div>
            <div class="image-wrapper">
                <img v-show="imageUrls.length > 0" :src="diagnosisImageUrl" alt="检测结果图像" class="post-diagnosis" />
                <!-- <img v-show="imageUrls.length > 0" :src="diagnosisImageUrl" alt="检测结果图像" class="post-diagnosis"
                    v-if="DiagnosisStore.diagnosisImg === ''" />
                <img :src="DiagnosisStore.diagnosisImg" alt="检测结果图像" class="post-diagnosis" v-else /> -->
            </div>
        </div>
        <div class="eventButton">
            <div class="navigation-buttons" v-show="imageUrls.length > 1">
                <button @click="prevImage">上一张</button>
                <button @click="nextImage">下一张</button>
            </div>
            <button class="upload-button" @click="triggerFileUpload">选择图像</button>
        </div>
    </div>
</template>

<script setup lang='ts'>
import { ref } from 'vue';
import axios from 'axios';
import { onMounted } from 'vue';
// import useDiagnosisStore from '../store/diagnosis';
// const DiagnosisStore = useDiagnosisStore();


const imageUrls = ref<string[]>([]);
const currentIndex = ref(0);
const fileInput = ref<HTMLInputElement | null>(null);
const diagnosisImageUrl = ref<string | null>(null);

const onFileChange = async (event: Event) => {
    const files = (event.target as HTMLInputElement).files;
    if (files) {
        imageUrls.value = Array.from(files).map(file => URL.createObjectURL(file));
        currentIndex.value = 0;

        // 上传图片并保存到服务器
        const formData = new FormData();
        formData.append('file', files[0], 'pt.jpg');
        await axios.post('/upload', formData);

        // 运行 Python 脚本
        await axios.post('/run-script');

        // 更新右侧的图片
        diagnosisImageUrl.value = '/output/feature_map_layer_0.png';

        // DiagnosisStore.saveImg(imageUrls.value[0], diagnosisImageUrl.value);

    }
};

const triggerFileUpload = () => {
    fileInput.value?.click();
};

const prevImage = () => {
    if (currentIndex.value > 0) {
        currentIndex.value--;
    }
};

const nextImage = () => {
    if (currentIndex.value < imageUrls.value.length - 1) {
        currentIndex.value++;
    }
};
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

        .navigation-buttons {
            width: 100%;
            font-size: 2.5vh;
            height: 30%;
            display: flex;
            justify-content: center;
            align-items: center;

            button {
                background-color: skyblue;
                margin-right: 2vh;
                text-align: center;
                border-radius: 5px;
                padding: 0.6vh 1.4vh;
            }

            button:hover {
                background-color: green;
                color: white;
            }
        }
    }
}
</style>