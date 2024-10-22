<script setup name="OAPagination">
import { defineModel, defineProps } from "vue";
import { ref, reactive, onMounted, watch } from "vue";
let props = defineProps({
  total: {
    type: Number,
    default: 0,
  },
  pageSize: {
    type: Number,
    default: 10,
  },
});

let page = defineModel({ required: true });
let page_size = ref(0);
</script>

<template>
  <div style="display: flex; justify-content: space-between">
    <el-form-item label="page:">
      <el-select v-model="page_size" size="small" style="width: 100px">
        <el-option select label="8 item/page" :value="8" />
        <el-option label="64 item/page" :value="64" />
      </el-select>
    </el-form-item>
    <el-pagination
      background
      layout="prev, pager, next"
      :total="props.total"
      :page-size="props.pageSize"
      v-model:current-page="page"
    />
  </div>
</template>

<style scoped>
.el-pagination {
  justify-content: center;
}
</style>
