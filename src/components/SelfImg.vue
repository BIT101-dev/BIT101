<!--
 * @Author: flwfdd
 * @Date: 2022-03-16 22:28:42
 * @LastEditTime: 2022-03-16 22:36:06
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-img :src="src?$store.state.img_url+src:''">
    <template v-slot:placeholder>
        <v-row
          class="fill-height ma-0"
          align="center"
          justify="center"
        >
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
  </v-img>
</template>

<script>
export default {
    name:"SelfImg",
    props: ['src'],
}
</script>