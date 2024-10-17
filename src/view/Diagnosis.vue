<template>
    <div class="diagnosis">
        <input type="file" ref="fileInput" @change="onFileChange" style="display: none;" multiple />
        <div class="images-container">
            <div class="image-wrapper">
                <img v-show="imageUrls.length > 0" :src="imageUrls[currentIndex]" alt="Uploaded Image" />
            </div>
            <div class="image-wrapper">
                <img v-show="imageUrls.length > 0" src="../assets/feature_map_layer_0.png" alt="检测结果图像"
                    class="post-diagnosis" />
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

const imageUrls = ref<string[]>([]);
const currentIndex = ref(0);
const fileInput = ref<HTMLInputElement | null>(null);

const onFileChange = (event: Event) => {
    const files = (event.target as HTMLInputElement).files;
    if (files) {
        imageUrls.value = Array.from(files).map(file => URL.createObjectURL(file));
        currentIndex.value = 0;
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
        // background-color: yellow;
        // margin-top: 20px;
        display: flex;
        justify-content: space-around;

        .image-wrapper {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            /* 防止出现滚动条 */

            img {
                max-width: 90%;
                max-height: 90%;
                min-height: 90%;
                min-width: 90%;
                object-fit: contain;
                /* 保持图片的纵横比 */
            }

            // .post-diagnosis {
            //     margin-left: 5px;
            //     transform: scaleX(-1);
            // }
        }
    }

    .eventButton {
        padding: 1%;
        height: 15%;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        // justify-content: space-between;
        // background-color: pink;

        .upload-button {
            margin-top: 7vh;
            width: 25%;
            // background-color: blue;
            // color: white;
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
                /* 调整 padding 以增加按钮内部的空隙 */
                // line-height: 2.5vh;
                /* 确保文字垂直居中 */
            }

            button:hover {
                background-color: green;
                color: white;
            }
        }
    }


}
</style>