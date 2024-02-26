<!--
 * @Author: flwfdd
 * @Date: 2023-10-28 12:27:23
 * @LastEditTime: 2024-02-26 17:17:34
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import store from '@/utils/store';
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { setTitle } from '@/utils/tools';
import { Claim, Image, Poster } from '@/utils/types';
import { AddRound } from '@vicons/material';
import { UploadFileInfo } from 'naive-ui';

const route = useRoute();
const router = useRouter();

const report = reactive({
  title: "",
  text: "",
  posting: false,
  types: [] as { label: number, value: string }[],
  type_id: null,
})

function PostReport() {
  if (report.type_id == null) {
    window.$message.error("请选择举报类别Orz");
    return;
  }
  if (report.text.length == 0) {
    window.$message.error("请填写举报理由Orz");
    return;
  }
  report.posting = true;
  http.post("/manage/reports", {
    obj: route.params.obj,
    type_id: report.type_id,
    text: report.text
  }).then(() => {
    router.go(-1);
  }).finally(() => {
    report.posting = false;
  })
}

function GetReportTypes() {
  http.get("/manage/report_types").then((res) => {
    report.types = res.data.map((i: any) => { return { label: i.text, value: i.id } });
  })
}

onMounted(() => {
  GetReportTypes();
  if (route.params.obj) {
    let obj = route.params.obj.toString();
    if (obj.startsWith("poster")) {
      report.title = "举报Poster";
    }
    if (obj.startsWith("comment")) {
      report.title = "举报评论";
    }
  }
})

</script>

<template>
  <div class="container">
    <n-space vertical size="large">
      <n-h2 style="margin-top:0px;margin-bottom:-6px;">{{ report.title }}</n-h2>

      <n-space vertical size="small">
        <div>举报类别</div>
        <n-select v-model:value="report.type_id" :options="report.types" />
      </n-space>

      <n-space vertical size="small">
        <div>举报理由</div>
        <n-input v-model:value="report.text" type="textarea" placeholder="请输入内容" :autosize="{ minRows: 6 }"
          maxlength="23333" show-count />
      </n-space>

      <n-space justify="end">
        <n-popconfirm @positive-click="PostReport" :show-icon="false" positive-text="确定" negative-text="取消">
          <template #trigger>
            <n-button :disabled="report.posting" type="success" ghost>举报</n-button>
          </template>
          汝真举报耶？
        </n-popconfirm>
      </n-space>
    </n-space>

  </div>
</template>