<!--
 * @Author: flwfdd
 * @Date: 2022-07-30 14:05:26
 * @LastEditTime: 2024-02-26 16:47:53
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import { reactive, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { UploadCustomRequestOptions, UploadInst } from 'naive-ui'
import UploadRound from '@vicons/material/UploadRound'
import http from '@/utils/request'
import { OpenLink, setTitle } from '@/utils/tools'
import axios from 'axios'

const course = reactive({
  id: "",
  number: "",
  name: "",
  type: "other",
  msg: ""
})

const is_removed = {};
function customRequest({
  file,
  onFinish,
  onError,
  onProgress
}: UploadCustomRequestOptions) {
  http.get('/courses/upload/url', {
    params: {
      number: course.number,
      type: course.type,
      name: file.name
    }
  }).then(async res => {
    let url = res.data.url;
    let status = true;
    if (file.file) {
      let size = file.file.size;
      let chunk_size = 3276800;
      let uploaded_size = 0;
      let log_id = res.data.id;
      for (let i = 0; i < size; i += chunk_size) {
        if (is_removed[file.id]) {
          onError();
          status=false;
          break;
        }
        let chunk_data = file.file.slice(i, i + chunk_size);
        let head = {
          // 'Content-Length': chunk_data.size,
          'Content-Range': `bytes ${i}-${i + chunk_data.size - 1}/${size}`,
          'Content-Type': 'text/plain'
        }
        
        await axios.put(url, chunk_data, {
          headers: head,
          onUploadProgress: (progress) => {
            onProgress({ 'percent': (progress.loaded + uploaded_size) / size * 100 })
          }
        }).then(() => { uploaded_size += chunk_data.size })
          .catch(() => { status = false })
        if (!status) {
          onError();
          break;
        }
      }

      //上传记录
      if(status)http.post('/courses/upload/log', { 'id': log_id, 'msg': course.msg })
        .then(() => { onFinish() }).catch(() => { onError() })
    }
    else onError();
  }).catch(() => { onError() })
}

function removeHandler({
  file
}: UploadCustomRequestOptions) {
  is_removed[file.id] = true;
}

const uploadRef = ref<UploadInst | null>(null);
function Submit() {
  uploadRef.value?.submit()
}

function LoadCourse() {
  return http.get('/courses/' + course.id).then(res => {
    let data = res.data;
    course.name = data.name;
    course.number = data.number;
  })
}

const route = useRoute();
course.id = route.params.id as string;
onMounted(async () => {
  await LoadCourse()
  setTitle('上传资料', course.name, '课程')
})
</script>

<template>
  <div class="container">
    <h2 style="color:var(--text-color-1);">{{ course.name }} 共享资料上传</h2>

    <n-space vertical>
      <n-alert type="info" title="Tips" closable>
        上传前请先看看是否已经有相同资料了，有就不要重复上传啦QwQ<br />
        非常感谢您的贡献_(:з」∠)_
        <div style="font-size:14px;">
          关于类别的说明：<br />
          书籍：教科书、课程相关电子书等<br />
          课件：PPT什么的<br />
          考试：考试相关的往年题、复习资料等<br />
          其他：兜底条款，比如作业资料....？<br />
        </div>
      </n-alert>

      <n-button @click="OpenLink(`https://onedrive.bit101.cn/zh-CN/course/${course.name}-${course.number}`)" block ghost>
          查看课程资料
        </n-button>

      <n-radio-group v-model:value="course.type">
        <n-space>
          类别：
          <n-radio value="book">书籍</n-radio>
          <n-radio value="ppt">课件</n-radio>
          <n-radio value="exam">考试</n-radio>
          <n-radio value="other">其他</n-radio>
        </n-space>
      </n-radio-group>

      <n-upload multiple :custom-request="customRequest" :on-remove="removeHandler" ref="uploadRef"
        :default-upload="false">
        <n-upload-dragger>
          <div style="margin-bottom: 11px">
            <n-icon size="48" :depth="3">
              <UploadRound />
            </n-icon>
          </div>
          <div>
            点击或者拖动文件到该区域来选择文件
          </div>
        </n-upload-dragger>
      </n-upload>
      <n-input v-model:value="course.msg" type="textarea" maxlength="2244"
        placeholder="你可以留下你的名字、关于资料的备注等，这段文字将会出现在共享资料网页中。"></n-input>
      <n-button @click="Submit" block>上传</n-button>
    </n-space>
  </div>
</template>