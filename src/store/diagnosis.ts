// // store/diagnosis.ts
// import { defineStore } from 'pinia';
// import { ref } from 'vue';
// import axios from 'axios';

// export const useDiagnosisStore = defineStore('diagnosis', () => {
//     const imageUrls = ref<string[]>([]);
//     const currentIndex = ref(0);
//     const diagnosisImageUrl = ref<string | null>(null);

//     const onFileChange = async (event: Event) => {
//         const files = (event.target as HTMLInputElement).files;
//             // 更新右侧的图片
//             diagnosisImageUrl.value = '/output/feature_map_layer_0.png';

//             // 将图片 URL 保存到本地存储
//             localStorage.setItem('imageUrls', JSON.stringify(imageUrls.value));
//             localStorage.setItem('diagnosisImageUrl', diagnosisImageUrl.value);
//     };

//     const loadFromLocalStorage = () => {
//         const storedImageUrls = localStorage.getItem('imageUrls');
//         const storedDiagnosisImageUrl = localStorage.getItem('diagnosisImageUrl');
//         if (storedImageUrls) {
//             imageUrls.value = JSON.parse(storedImageUrls);
//         }
//         if (storedDiagnosisImageUrl) {
//             diagnosisImageUrl.value = storedDiagnosisImageUrl;
//         }
//     };

//     return {
//         imageUrls,
//         currentIndex,
//         diagnosisImageUrl,
//         onFileChange,
//         loadFromLocalStorage
//     };
// });



//定义用户相关的仓库

import { defineStore } from "pinia";
const useDiagnosisStore = defineStore('user', {
    state: () => ({
        orignImg: localStorage.getItem('orignImg') ? JSON.parse(localStorage.getItem('orignImg') as string) : '',
        diagnosisImg: localStorage.getItem('diagnosisImg') ? JSON.parse(localStorage.getItem('diagnosisImg') as string) : ''
    }),
    actions: {
        //获取验证码的方法
        async saveImg(orignImg: string, diagnosisImg: string) {
            // userInfo: localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo') as string) : {} //存储用户的信息，如果本地有存储，则从本地拿，没有则为空
            this.orignImg = orignImg
            this.diagnosisImg = diagnosisImg
            localStorage.setItem('orignImg', JSON.stringify(this.orignImg));
            localStorage.setItem('diagnosisImg', JSON.stringify(this.diagnosisImg));
        }
    },
    getters: {}
})
export default useDiagnosisStore