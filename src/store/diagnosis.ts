import { defineStore } from "pinia";
const useDiagnosisStore = defineStore('diagnosis', {
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
export default useDiagnosisStore