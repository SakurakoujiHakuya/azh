<script setup lang="ts">
import LoginInput from "../components/LoginInput.vue";
import { useRouter } from "vue-router";
import { ElMessage } from 'element-plus'
const router = useRouter();

const handleLogin = () => {
  router.push('/mainBoard/diagnosis');
  ElMessage({
    message: 'Wellcome administrator!.',
    type: 'success',
  })
}

</script>

<template>

  <div id="login-wrapper">
    <div id="login-container">
      <div id="login-box">
        <span id="login-title">LOGIN</span>
        <div id="input-box">
          <LoginInput text="手机号" />
          <LoginInput text="密码" />
        </div>
        <div @click="handleLogin" id="login-button-container">
          <span id="login-button-text">登录</span>
          <div id="login-button-background"></div>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped lang="scss">
#login-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #121212;

  background-image: radial-gradient(closest-side, #0fb69d 0%, #12121200 70%),
    radial-gradient(closest-side, #39b60f 0%, #12121200 80%),
    radial-gradient(closest-side, #ec7805 0%, #12121200 75%);
  background-size: 100vmax 100vmax, 120vmax 120vmax, 100vmax 100vmax;
  background-repeat: no-repeat;



  animation: background01-shine 8s ease-in-out alternate infinite;
}

@keyframes background01-shine {
  0% {
    background-position: -38vmax -54vmax, -41vmax -24vmax, 30vmax -24vmax;
  }

  50% {
    background-position: 10vmax -35vmax, -38vmax -54vmax, 24vmax -16vmax;
  }

  100% {
    background-position: -41vmax -24vmax, 6vmax -12vmax, 20vmax -24vmax;
  }
}

@keyframes background02-shine {
  0% {
    background-position: 50% 50%;
  }

  50% {
    background-position: 23% 85%;
  }

  100% {
    background-position: 20% 48%;
  }
}

#login-container {
  width: 60vw;
  height: 90vh;
  border-radius: 50px;
  background-color: #2c2c2c;
}

#login-box {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#login-title {
  color: #fff;
  font-size: 2em;
  font-weight: 800;
  letter-spacing: 5px;
  font-family: 'Microsoft New Tai Lue', serif;
}

#input-box {
  margin-top: 100px;
  margin-bottom: 60px;
}

#login-button-container {
  width: 220px;
  height: 40px;
  border-radius: 25px;
  background-color: white;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;

  &:hover {
    cursor: pointer;
  }
}

#login-button-background {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  background-color: rgba(82, 186, 0, 1);
  clip-path: circle(0 at 20% 50%);

  transition: clip-path .3s ease-in-out;
}

#login-button-text {
  color: #000;
  font-size: 1.4em;
  font-weight: 800;
  z-index: 110;
}

#login-button-container:hover #login-button-background {
  clip-path: circle(200% at 50% 50%);
}
</style>