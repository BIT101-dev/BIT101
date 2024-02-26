<!--
 * @Author: flwfdd
 * @Date: 2023-05-14 12:54:39
 * @LastEditTime: 2024-02-26 17:11:50
 * @Description: _(:з」∠)_
-->
<script setup>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LControl } from "@vue-leaflet/vue-leaflet";
import { ref } from "vue";

const liang_xiang_center = [39.72978, 116.16659];
const zhong_guan_cun_center = [39.95779, 116.30980];

const zoom = ref(16);
const center = ref(liang_xiang_center);

function MoveTo(x) {
    center.value = x;
}

</script>

<template>
    <div style="height:100vh; width:100%;">
        <l-map ref="map" v-model:zoom="zoom" :center="center" :use-global-leaflet="false">
            <l-tile-layer url="https://map.bit101.flwfdd.xyz/tile/{z}/{x}/{y}.png"></l-tile-layer>
            <l-control class="leaflet-control" position="topright">
                <n-button-group>
                    <n-button @click="MoveTo(liang_xiang_center)" type="primary">乡</n-button>
                    <n-button @click="MoveTo(zhong_guan_cun_center)" type="primary">村</n-button>
                </n-button-group>

            </l-control>
        </l-map>
    </div>
</template>