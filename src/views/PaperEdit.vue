<!--
 * @Author: flwfdd
 * @Date: 2022-06-28 20:46:23
 * @LastEditTime: 2022-06-29 00:38:45
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import EditorJS from '@editorjs/editorjs';
import Header from '@editorjs/header';
import Raw from '@editorjs/raw';
import Image from '@editorjs/image';
import List from '@editorjs/list';
import Code from '@editorjs/code';
import http from '@/utils/request';
import store from '@/utils/store';

//通过文件上传图片
function UploadFile(file: File) {
  let param = new FormData();
  param.append('file', file)
  let config = {
    headers: {
      'Content-Type': 'multipart/form-data',
      'fake-cookie': store.fake_cookie,
    }
  }
  return http.post('/upload/image/', param, config)
    .then((res) => {
      return {
        success: true,
        file: {
          url: res.data.url
        }
      }
    })
}

//通过url上传图片
function UploadUrl(url: string) {
  let param = {  url: url  };
  let config = {
    headers: {
      'fake-cookie': store.fake_cookie,
    }
  }
  return http.post('/upload/image/', param, config)
    .then((res) => {
      return {
        success: true,
        file: {
          url: res.data.url
        }
      }
    })
}

const editor = new EditorJS({
  holder: 'editorjs',
  tools: {
    header: Header,
    image: {
      class: Image,
      config: {
        uploader: {
          uploadByFile: UploadFile,
          uploadByUrl: UploadUrl,
        }
      }
    },
    list: List,
    code: Code,
    raw: Raw,
  }
});
</script>

<template>
  <div class="editor_container">
    <n-card title="文章编辑">
      asdf
    </n-card>
    <n-divider>
    ↓编辑区↓
  </n-divider>
    <div id="editorjs"></div>
  </div>
</template>

<style>
.editor_container {
  max-width: 700px;
  margin: auto;
}
</style>