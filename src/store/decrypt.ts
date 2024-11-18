import { defineStore } from "pinia";
const useDecryptStore = defineStore('decrypt', {
    state() {
        return {
            leftImg: "",//左侧图片
            rightImg: "",//右侧图片
        }
    },
    actions: {
    },
    getters: {}
})
export default useDecryptStore