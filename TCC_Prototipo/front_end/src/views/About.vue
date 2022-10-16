<template>
  <div class="about">
    <router-link to="/">Home</router-link>
    <h1>{{ name }}</h1>
  </div>
</template>

<script>
import { value } from './Home.vue'

export default {
  data: function () {
    return {
      name: value,
    };
  }
};

</script>

