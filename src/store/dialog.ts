import { keysOf } from "element-plus/es/utils/objects.mjs";
import { defineStore } from "pinia";
import { isQuestionOrPlusOrMinusToken } from "typescript";
const useDialogStore = defineStore('user', {
    state() {
        return {
            visiable: false,//用于控制key输入框的dialog显示与隐藏
            key: "0.11, 0.12",//原来的key值
            inputKey: "0.11, 0.12",//用于存储key输入框的值
        }
    },
    actions: {
    },
    getters: {}
})
export default useDialogStore