<!--
 * @Author: flwfdd
 * @Date: 2022-03-16 21:28:13
 * @LastEditTime: 2022-03-16 22:20:35
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-card>
    <v-card-title>上传</v-card-title>
    <v-card-text>
      <v-file-input
        v-if="progress == 0"
        label="选择"
        v-model="files"
        prepend-icon="attach_file"
        multiple
        chips
        counter
        show-size
        color="cyan"
      ></v-file-input>
      <v-btn v-if="progress == 0" block color="cyan lighten-4" @click="Upload"
        ><v-icon color="cyan accent-4">file_upload</v-icon></v-btn
      >
      <v-progress-linear
        v-if="progress != 0"
        :value="progress * 100"
        height="24"
        color="pink lighten-4"
        stream
        buffer-value="0"
        rounded
      >
        <template v-slot="{ value }">
          <strong class="cyan--text text--accent-4"
            >{{ Math.ceil(value * 100) / 100 }}%</strong
          >
        </template>
      </v-progress-linear>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "UploadImage",
  data: () => ({
    files: [],
    progress: 0,
  }),
  methods: {
    Upload() {
      if (this.files.length == 0) {
        this.$store.commit('msg','空空如也呢qwq');
        return;
      }
      let form = new FormData();
      for (let i in this.files) {
        form.append("files", this.files[i]);
      }

      let config = {
        onUploadProgress: (e) => {
          this.progress = e.loaded / e.total;
        },
      };
      this.$axios
        .post(this.$store.state.api_url+"/upload_image/", form, config)
        .then((res) => {
          this.upfile = [];
          this.progress = 0;
          this.$store.commit('msg','上传成功OvO');
          this.$emit('uploaded', res.data);
        })
        .catch((err) => {
          this.progress=0;
          this.$store.commit('msg','出错了Orz');
          console.log(err);
        });
    },
  },
};
</script>