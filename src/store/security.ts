import { defineStore } from "pinia";
const useSecurityStore = defineStore('security', {
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
export default useSecurityStore