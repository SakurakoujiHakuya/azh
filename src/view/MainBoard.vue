<template>
  <div class="container">
    <div class="menu">
      <functionMenu />
    </div>
    <div class="right">
      <topbar />
      <!-- <show /> -->
      <div class="content">
        <router-view></router-view>
      </div>
      <bottom />
    </div>
  </div>

</template>

<script setup lang='ts'>
import topbar from '../components/topbar.vue';
import bottom from '../components/bottom.vue';
import functionMenu from '../components/functionMenu.vue';
</script>

<style lang="scss" scoped>
.container {
  // margin: 10px;
  display: flex;
  // background-color: rgb(29, 34, 56);
  background-color: beige;
  width: 100vw;
  height: 100vh;

  .menu {
    height: 100%;
    flex: 2;
    // margin: 0 0.5%;
  }

  .right {
    width: 100%;
    height: 100%;
    flex: 8;
    display: flex;
    flex-direction: column;

    .content {
      height: 84vh;
      // background-color: skyblue;
    }
  }
}
</style>