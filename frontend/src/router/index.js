import { createRouter, createWebHashHistory } from "vue-router";
import login from "@/views/login/login.vue";
import frame from "@/views/main/frame.vue";
import { useAuthStore } from "@/stores/auth";
import calibration from "@/views/cb22/calibration.vue";
import home from "@/views/home/home.vue";
import ttmodel from "@/views/threedmodel/ttmodel.vue";
import ttcalibration from "@/views/ttcalibration/ttcalibration.vue";
const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "frame",
      component: frame,
      children: [
        {
          path: "/cb22/calibration",
          name: "calibration",
          component: calibration,
        },
        {
          path: "/",
          name: "home",
          component: home,
        },
        {
          path: "/threedmodel/ttmodel",
          name: "ttmodel",
          component: ttmodel,
        },
        {
          path: "/ttcalibration/ttcalibration",
          name: "ttcalibration",
          component: ttcalibration,
        },
      ],
    },
    {
      path: "/login",
      name: "login",
      component: login,
    },
  ],
});
router.beforeEach((to, from) => {
  // 判断用户是否登录，如果没有登录
  // 并且访问的页面不是登录页面，那么就要跳转到登录页面
  const authStore = useAuthStore();
  if (!authStore.is_logined && to.name != "login") {
    return { name: "login" };
  }
});

export default router;
