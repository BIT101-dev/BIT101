<!--
 * @Author: flwfdd
 * @Date: 2022-06-28 20:46:23
 * @LastEditTime: 2022-07-06 21:38:06
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import EditorJS from '@editorjs/editorjs';
import Header from '@editorjs/header';
import Image from '@editorjs/image';
import List from '@editorjs/list';
import Code from '@editorjs/code';
import Quote from '@editorjs/quote';
import Delimiter from '@editorjs/delimiter';
import Table from '@editorjs/table';
import InlineCode from '@editorjs/inline-code'
import AnyButton from 'editorjs-button'
import Undo from 'editorjs-undo';
import http from '@/utils/request';
import store from '@/utils/store';
import { onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import PaperRender from '@/components/PaperRender.vue';

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
  let param = { url: url };
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

//实例化编辑器
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
    quote: Quote,
    code: Code,
    AnyButton: AnyButton,
    delimiter: Delimiter,
    table: Table,
    inlineCode: {
      class: InlineCode
    },
  },
  i18n: { //翻译
    messages: {
      toolNames: {
        Text: "文本",
        Heading: "标题",
        Image: "图片",
        List: "列表",
        Quote: "引言",
        Code: "代码",
        Button: "链接",
        Delimiter: "分割",
        Table: "表格"
      }
    },
  },
  onReady:()=>{
    new Undo({editor});
  }
});

//文章数据
const paper = reactive({
  id: "",
  title: "俺是标题！",
  intro: "",
  data: {},
})

//预览文章
const modal = ref(false)
function PreviewPaper() {
  editor.save().then((out) => {
    paper.data = out;
    modal.value = true;
  }).catch(err => { console.log(err) })
}

//加载文章
function LoadPaper() {
  paper.id = route.params.id as string;
  if (paper.id == '0') return;
}

const route = useRoute();
onMounted(() => {
  LoadPaper();
})
</script>

<template>
  <div class="container">
    <n-card :title="paper.id == '0' ? '新建文章' : '修改文章' + paper.id">
      <n-space vertical>
        <div>标题</div>
        <n-input v-model:value="paper.title" placeholder="请输入标题" maxlength="42" show-count size="large"></n-input>
        <div>简介（为空则根据文章自动生成）</div>
        <n-input v-model:value="paper.intro" placeholder="请输入简介" maxlength="224" show-count></n-input>
        <n-button @click="PreviewPaper">预览</n-button>
      </n-space>
    </n-card>
    <br />
    <div id="editorjs"></div>
    <br />
    <br />
    <n-modal v-model:show="modal" preset="card" style="width:666px">
        <PaperRender :paper="paper" />
    </n-modal>

  </div>
</template>