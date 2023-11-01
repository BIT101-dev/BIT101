<!--
 * @Author: flwfdd
 * @Date: 2022-06-28 20:46:23
 * @LastEditTime: 2023-11-01 22:51:08
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
import { useRoute, useRouter } from 'vue-router';
import PaperRender from '@/components/PaperRender.vue';
import { setTitle } from '@/utils/tools';

//文章数据
const paper = reactive({
  id: "",
  title: "俺是标题！",
  intro: "",
  data: {},
  last_time: 0,
  anonymous: false,
  public_edit: true,
  own: true,
})

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
  return http.post('/upload/image', param, config)
    .then((res) => {
      return {
        success: true,
        file: {
          url: res.data.url,
          low_url: res.data.low_url,
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
  return http.post('/upload/image/url', param, config)
    .then((res) => {
      return {
        success: true,
        file: {
          url: res.data.url,
          low_url: res.data.low_url,
        }
      }
    })
}

//实例化编辑器
let editor: EditorJS;
function InitEditor(init_paper = false) {
  editor = new EditorJS({
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
    onReady: () => {
      let undo = new Undo({ editor });
      if (init_paper && paper.data.blocks.length) {
        editor.render(paper.data);
        undo.initialize(paper.data);
      }
      editor.focus();
    }
  });
}

//预览文章
const modal = ref(false)
function PreviewPaper() {
  editor.save().then((out) => {
    paper.data = out;
    modal.value = true;
  }).catch(err => {
    window.$message.error("预览失败Orz");
  })
}

//加载文章
function LoadPaper() {
  paper.id = route.params.id as string;
  if (paper.id == '0') InitEditor(false);
  else return http.get("/papers/" + paper.id)
    .then(res => {
      paper.title = res.data.title;
      paper.intro = res.data.intro;
      paper.data = JSON.parse(res.data.content);
      paper.last_time = new Date(res.data.update_time).getTime() / 1000;
      paper.anonymous = res.data.anonymous;
      paper.public_edit = res.data.public_edit;
      paper.own = res.data.own;
      InitEditor(true);
    })
}

const route = useRoute();
const router = useRouter();
onMounted(async () => {
  await LoadPaper()
  setTitle('编辑', paper.title, '文章')
})

//发表文章
const posting = ref(false);
function PostPaper() {
  posting.value = true;
  editor.save().then((data) => {
    //生成简介
    if (!paper.intro) {
      let max_lenth = 124;
      for (let i of data.blocks) {
        if (i.type == 'paragraph' || i.type == 'header' || i.type == 'quote') {
          paper.intro += i.data.text.slice(0, max_lenth - paper.intro.length) + " ";

        }
        else if (i.type == 'list') {
          for (let j of i.data.items) paper.intro += j.slice(0, max_lenth - paper.intro.length) + " ";
        }
        if (paper.intro.length >= max_lenth) break;
      }
    }

    let paper_data = {
      title: paper.title,
      intro: paper.intro,
      content: JSON.stringify(data),
      last_time: paper.last_time,
      anonymous: paper.anonymous,
      public_edit: paper.public_edit,
    }

    if (paper.id == '0') {
      http.post("/papers", paper_data).then((res) => {
        posting.value = false;
        router.push('/paper/' + res.data.id);
      }).catch(() => {
        posting.value = false;
      })
    } else {
      http.put("/papers/" + paper.id, paper_data).then(() => {
        posting.value = false;
        router.push('/paper/' + paper.id);
      }).catch(() => {
        posting.value = false;
      })
    }
  })
}

// 删除文章
function DeletePaper() {
  http.delete("/papers/" + paper.id).then(() => {
    router.push('/paper/');
  })
}

</script>

<template>
  <div class="container">
    <n-card :title="paper.id == '0' ? '新建 Paper' : '编辑 Paper ' + paper.id">
      <n-space vertical>
        <div>标题</div>
        <n-input v-model:value="paper.title" placeholder="请输入标题" maxlength="42" show-count size="large"></n-input>
        <div>简介（为空则根据文章自动生成）</div>
        <n-input v-model:value="paper.intro" placeholder="请输入简介" maxlength="101" show-count clearable></n-input>
        <n-space>
          <n-button @click="PreviewPaper" type="info" ghost>预览</n-button>
          <n-popconfirm @positive-click="PostPaper" :show-icon="false" positive-text="确定" negative-text="取消">
            <template #trigger>
              <n-button :disabled="posting" type="success" ghost>发Paper</n-button>
            </template>
            汝真发表耶？
          </n-popconfirm>
          <n-button @click="paper.anonymous = !paper.anonymous" ghost>匿名:{{ paper.anonymous ? '是' : '否' }}</n-button>
          <n-button v-if="paper.own" @click="paper.public_edit = !paper.public_edit" ghost>其他人可编辑:{{ paper.public_edit ?
            '是' : '否' }}
          </n-button>
          <n-popconfirm v-if="paper.own" @positive-click="DeletePaper" :show-icon="false" positive-text="确定"
            negative-text="取消">
            <template #trigger>
              <n-button :disabled="posting" type="error" ghost>删除</n-button>
            </template>
            汝真断舍离耶？
          </n-popconfirm>
        </n-space>
      </n-space>
    </n-card>

    <n-card style="margin: 11px 0 24px 0;">
      <div id="editorjs"></div>
    </n-card>

    <n-modal v-model:show="modal" preset="card" style="width:666px">
      <n-scrollbar style="max-height:88vh;">
        <PaperRender :paper="paper" />
      </n-scrollbar>
    </n-modal>

  </div>
</template>