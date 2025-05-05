<script setup lang="ts">

import { ref } from "vue";

const props = defineProps({
  text: {
    type: String,
    default: 'input'
  }
})

const inputRef = ref();
const spanRef = ref();
const inputValue = ref();
const isFocused = ref(false);
const isEmpty = ref(true);

let timeoutId: number | undefined;
const handleFocus = () => {
  timeoutId = setTimeout(() => {
    inputRef.value.style.caretColor = 'white';
  }, 200);

  inputRef.value.focus();
  isFocused.value = true;
  const width = spanRef.value.getBoundingClientRect().width + 10;
  spanRef.value.style.transform = `translate(${-width}px, 0)`;
}

const handleBlur = () => {
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
  inputRef.value.style.caretColor = 'transparent';

  inputRef.value.blur();
  isFocused.value = false;

  if (isEmpty.value) {
    spanRef.value.style.transform = `translate(5px, 0)`;
  }
}

const handleInput = (event:any) => {
  inputValue.value = event.target.value;

  isEmpty.value = inputValue.value === '';
}

</script>

<template>
  <div class="input-unit" @click="handleFocus">
    <span ref="spanRef" class="input-span"
      :class="[isFocused ? 'input-span-focused' : 'input-span-blurred']">{{ props.text }}</span>
    <input @blur="handleBlur" @input="handleInput" ref="inputRef" :value="inputValue" class="input" />
  </div>
</template>

<style scoped lang="scss">
.input-unit {
  width: 200px;
  position: relative;
  margin: 20px 0;
  padding: 5px 0;
  border-bottom: 1px solid #b5b5b5;
}

.input-span {
  font-size: .8em;
  position: absolute;
  top: 7px;

  transition: color .2s ease-in-out, transform .3s ease-in-out;
  transform: translate(5px, 0);
}

.input-span-blurred {
  color: rgba(82, 186, 0, 0.5);
}

.input-span-focused {
  color: #fff;
}

.input {
  all: unset;

  text-space: 5px;
  color: white;
  caret-color: transparent;
  padding-left: 5px;
  font-family: 'Microsoft New Tai Lue', serif;
}
</style>