<template>
    <div class="security">
        <input type="file" ref="fileInput" style="display: none;" multiple />
        <div class="images-container">
            <div class="image-wrapper">
                <img v-show="securityStore.leftImg !== ''" :src="securityStore.leftImg" alt="Uploaded Image" />
                <button v-show="securityStore.leftImg !== ''" @click="openImage(securityStore.leftImg)">打开图片</button>
            </div>
            <div class="image-wrapper">
                <img v-show="securityStore.rightImg !== ''" :src="securityStore.rightImg" alt="检测结果图像"
                    class="post-diagnosis" />
                <button v-show="securityStore.rightImg !== ''" @click="openImage(securityStore.rightImg)">打开图片</button>
            </div>
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
import useSecurityStore from '../store/security';
const securityStore = useSecurityStore();
const imageUrls = ref<string>(localStorage.getItem('imageUrls') || '');
const fileInput = ref<HTMLInputElement | null>(null);
const diagnosisImageUrl = ref<string | null>(localStorage.getItem('diagnosisImageUrl'));
const isLoading = ref<boolean>(false);

const openImage = (url: string | null) => {
    if (url) {
        window.open(url, '_blank');
    }
};


</script>

<style lang="scss" scoped>
.security {
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
                max-width: 92%;
                max-height: 92%;
                min-height: 92%;
                min-width: 92%;
                // object-fit: contain;
            }

            button {
                margin-top: 15px;
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