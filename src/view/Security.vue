<template>
    <button @click="test">点我</button>
    <MyDialog />
</template>

<script setup lang='ts'>
import useDialogStore from '../store/dialog';
import MyDialog from '../components/myDialog.vue';
const DialogStore = useDialogStore();
const test = () => {
    DialogStore.visiable = true
}
</script>

<style></style>
