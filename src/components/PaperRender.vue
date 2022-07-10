<!--
 * @Author: flwfdd
 * @Date: 2022-06-29 22:48:31
 * @LastEditTime: 2022-07-11 02:13:25
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import hljs from "highlight.js"
import "highlight.js/styles/vs2015.css"

defineProps(['paper'])

</script>

<style>
a {
  color: #FF8533;
}

b{
  font-weight: 900;
  color:#00293D;
}

.inline-code{
  background-color: rgba(250,239,240,0.78);
  color:#b44437;
  padding:3px 4px;
  border-radius: 5px;
  margin:0 1px;
  font-family: inherit;
}
</style>

<template>
  <div v-for="i in paper.data.blocks" style="word-wrap:break-word;">
    <!-- {{i.type}} -->
    <template v-if="i.type == 'paragraph'">
      <p style="color:#3E5C6B;" v-html="i.data.text"></p>
    </template>

    <template v-else-if="i.type == 'header'">
      <component :is="'h' + i.data.level" style="color:#FF8533;" v-html="i.data.text"></component>
    </template>

    <template v-else-if="i.type == 'image'">
      <div style="text-align:center;margin-top: 11px;margin-bottom: 11px;">
        <n-image :src="i.data.file.url" width="424" :img-props="{'style':'max-width:100%;'}" :alt="i.data.caption" />
        <div style="color:#6291A8" v-html="i.data.caption"></div>
      </div>
    </template>

    <template v-else-if="i.type == 'list'">
      <ol v-if="i.data.style == 'ordered'" style="color:#3E5C6B">
        <li v-for="j in i.data.items" v-html="j"></li>
      </ol>
      <ul v-else style="color:#3E5C6B">
        <li v-for="j in i.data.items" v-html="j"></li>
      </ul>
    </template>

    <template v-else-if="i.type == 'quote'">
      <n-alert :show-icon="false">
        <div style="color:#809BA8;font-size:42px;margin:-11px 0 0 -24px;">“</div>
        <div v-html="i.data.text" style="color:#3E5C6B;margin:-42px 24px 0 24px;"
          :style="'text-align:' + i.data.alignment"></div>
        <div style="color:#809BA8;text-align: right;font-size:42px;margin:-24px -20px -24px 0;">”</div>
        <div v-html="'——' + i.data.caption" style="color:#3E5C6B;text-align:right;"></div>
      </n-alert>
    </template>

    <template v-else-if="i.type == 'code'">
      <pre><code v-html="hljs.highlightAuto(i.data.code).value" class="hljs" style="border-radius:11px"></code></pre>
    </template>

    <template v-else-if="i.type == 'AnyButton'">
      <a :href="i.data.link" target="_blank">
        <n-card size="small">
          {{ i.data.text }}
          <div style="color:#809BA8;font-size: 11px;">{{ i.data.link }}</div>
        </n-card>
      </a>
    </template>

    <template v-else-if="i.type=='delimiter'">
      <n-divider></n-divider>
    </template>

    <template v-else-if="i.type=='table'">
      <n-table :single-line="false" striped size="small">
        <tbody>
          <tr v-for="row in i.data.content"><td v-for="j in row" v-html="j"></td></tr>
        </tbody>
      </n-table>
    </template>
  </div>
</template>