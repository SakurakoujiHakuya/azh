<template>
    <div class="diagnosis">
        <input type="file" ref="fileInput" @change="onFileChange" style="display: none;" />
        <div class="images-container">
            <div class="image-wrapper">
                <img v-if="imageUrl" :src="imageUrl" alt="Uploaded Image" />
            </div>
            <!-- 下面是诊断后的图像 -->
            <div class="image-wrapper">
                <img v-if="imageUrl" :src="imageUrl" alt="Mirrored Image" class="post-diagnosis" />
            </div>
        </div>
        <button class="upload-button" @click="triggerFileUpload">提交图片</button>
    </div>
</template>

<script setup lang='ts'>
import { ref } from 'vue';

const imageUrl = ref<string | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);

const onFileChange = (event: Event) => {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
        imageUrl.value = URL.createObjectURL(file);
    }
};

const triggerFileUpload = () => {
    fileInput.value?.click();
};
</script>

<style lang="scss" scoped>
.diagnosis {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    // height: 100vh;
    overflow: hidden;
    /* 防止出现滚动条 */

    .images-container {
        margin-top: 20px;
        display: flex;
        justify-content: space-around;
        width: 100%;
        flex: 1;
        /* 使图片容器占满剩余空间 */
        overflow: hidden;
        /* 防止出现滚动条 */

        .image-wrapper {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            /* 防止出现滚动条 */

            img {
                max-width: 95%;
                max-height: 95%;
                object-fit: contain;
                /* 保持图片的纵横比 */
            }

            .post-diagnosis {
                margin-left: 5px;
                transform: scaleX(-1);
            }
        }
    }

    .upload-button {
        width: 20vw;
        background-color: blue;
        color: white;
        padding: 10px 20px;
        cursor: pointer;
        border-radius: 5px;
        position: absolute;
        bottom: 10%;
        font-size: 2vw;
    }

    .upload-button:hover {
        background-color: darkblue;
    }
}
</style>