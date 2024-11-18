import { defineStore } from "pinia";
const useEncipherStore = defineStore('encipher', {
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
export default useEncipherStore