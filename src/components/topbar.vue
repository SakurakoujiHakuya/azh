<template>
    <div class="topbar">
        <span>用户：xxx</span>
        <img src="../assets/b_b8629520d4d314acb71cb637c0474dde.jpg" alt="">
    </div>
</template>

<script setup lang='ts'>

</script>

<style lang="scss" scoped>
.topbar {
    background-color: rgb(54, 65, 65);
    height: 10vh;
    padding: 0 5vw;
    display: flex;
    justify-content: end;
    align-items: center;

    span {
        color: white;
        font-size: 3vh;
    }

    img {
        margin-left: 6vw;
        width: 7vh;
        height: 7vh;
    }
}
</style>