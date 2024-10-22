<script setup name="frame">
import { ref, computed, reactive, onMounted } from "vue";
import { Expand, Fold } from "@element-plus/icons-vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import authHttp from "@/api/authHttp";
import { ElMessage } from "element-plus";
//import routes from "@/router/frame";

const authStore = useAuthStore();
const router = useRouter();

let displayUser = reactive({
  username: "",
});
let defaultActive = ref("home");
let isCollapse = ref(false);
let dialogVisible = ref(false);
let formLabelWidth = "100px";
let resetPwdForm = reactive({
  oldpwd: "",
  pwd1: "",
  pwd2: "",
});
let formTag = ref();
let rules = reactive({
  oldpwd: [
    { required: true, message: "请输入旧密码！", trigger: "blur" },
    { min: 6, max: 20, message: "密码长度需在6~20之间！", trigger: "blur" },
  ],
  pwd1: [
    { required: true, message: "请输入新密码！", trigger: "blur" },
    { min: 6, max: 20, message: "密码长度需在6~20之间！", trigger: "blur" },
  ],
  pwd2: [
    { required: true, message: "请输入确认密码！", trigger: "blur" },
    { min: 6, max: 20, message: "密码长度需在6~20之间！", trigger: "blur" },
  ],
});
let asideWidth = computed(() => {
  if (isCollapse.value) {
    return "63.99px";
  } else {
    return "200px";
  }
});

onMounted(() => {
  defaultActive.value = router.currentRoute.value.name;
  displayUser.username = authStore.user.uesrname;
});

const onCollapseAside = () => {
  isCollapse.value = !isCollapse.value;
};

const onExit = () => {
  authStore.clearUserToken();
  router.push({ name: "login" });
};

const onControlResetPwdDialog = () => {
  resetPwdForm.oldpwd = "";
  resetPwdForm.pwd1 = "";
  resetPwdForm.pwd2 = "";
  dialogVisible.value = true;
};

const onSubmit = () => {
  formTag.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        await authHttp.resetPwd(
          resetPwdForm.oldpwd,
          resetPwdForm.pwd1,
          resetPwdForm.pwd2
        );
        ElMessage.success("密码修改成功！");
        dialogVisible.value = false;
      } catch (detail) {
        ElMessage.error(detail);
      }
    } else {
      ElMessage.info("请按要求填写字段！");
    }
  });
};
</script>

<template>
  <el-container class="container">
    <el-aside class="aside" :width="asideWidth"
      ><router-link to="/" class="brand"
        ><strong>TT </strong
        ><span v-show="!isCollapse"> calibration</span></router-link
      >
      <el-menu
        :router="true"
        active-text-color="#ffd04b"
        background-color="#343a40"
        class="el-menu-vertical-demo"
        default-active="1"
        text-color="#fff"
        :collapse="isCollapse"
        :collapse-transition="false"
      >
        <el-menu-item index="1" :route="{ name: 'home' }">
          <el-icon><HomeFilled /></el-icon>
          <span>Home</span>
        </el-menu-item>
        <el-menu-item index="2" :route="{ name: 'calibration' }">
          <el-icon><HelpFilled /></el-icon>
          <span>CB22</span>
        </el-menu-item>
        <el-menu-item index="3" :route="{ name: 'ttcalibration' }">
          <el-icon><Notebook /></el-icon>
          <span>TT calibration</span>
        </el-menu-item>
        <el-menu-item index="4" :route="{ name: 'ttmodel' }">
          <el-icon><Grid /></el-icon>
          <span>3D model</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="left-header">
          <el-button
            v-show="isCollapse"
            :icon="Expand"
            @click="onCollapseAside"
          />
          <el-button
            v-show="!isCollapse"
            :icon="Fold"
            @click="onCollapseAside"
          />
        </div>
        <el-dropdown>
          <span class="el-dropdown-link">
            <el-avatar :size="30" icon="UserFilled" />
            <span style="margin-left: 10px">{{ authStore.user.username }}</span>
            <el-icon class="el-icon--right">
              <arrow-down />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="onControlResetPwdDialog"
                >modify code</el-dropdown-item
              >
              <el-dropdown-item divided @click="onExit"
                >log out</el-dropdown-item
              >
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <!-- <el-main>Main</el-main> -->
      <el-main><RouterView></RouterView></el-main>
    </el-container>
  </el-container>
  <el-dialog v-model="dialogVisible" title="修改密码" width="500">
    <el-form :model="resetPwdForm" :rules="rules" ref="formTag">
      <el-form-item label="旧密码" :label-width="formLabelWidth" prop="oldpwd">
        <el-input
          v-model="resetPwdForm.oldpwd"
          autocomplete="off"
          type="password"
        />
      </el-form-item>

      <el-form-item label="新密码" :label-width="formLabelWidth" prop="pwd1">
        <el-input
          v-model="resetPwdForm.pwd1"
          autocomplete="off"
          type="password"
        />
      </el-form-item>

      <el-form-item label="确认密码" :label-width="formLabelWidth" prop="pwd2">
        <el-input
          v-model="resetPwdForm.pwd2"
          autocomplete="off"
          type="password"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmit"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.container {
  height: 100vh;
}
.aside {
  background-color: #343a40;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22) !important;
}
.aside .brand {
  color: #fff;
  text-decoration: none;
  border-bottom: 1px solid #434a50;
  background-color: #232631;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}
.header {
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.el-dropdown-link {
  display: flex;
  align-items: center;
}

.el-menu {
  border-right: none;
}
</style>
