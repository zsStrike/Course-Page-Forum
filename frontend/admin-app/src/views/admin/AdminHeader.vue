<template>
  <el-row class="header" type="flex" justify="space-between">
    <el-col :span="2">
      <div class="center">
        <!-- In Vue tmplate, import an image is tricky， we use webpack require syntax here -->
        <div class="logo-img"
        :style="{ backgroundImage: 'url(' + require('@/assets/logo.png') + ')' }">
        </div>
      </div>
    </el-col>
    <el-col>
      <admin-nav-bar></admin-nav-bar>
    </el-col>
    <el-col :span="2">
      <div class="center">
        <el-dropdown placement="bottom" @command="commandHandler" size="medium">
          <el-avatar class="profile-img"
            src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="profile">个人资料</el-dropdown-item>
            <el-dropdown-item command="logout">登出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-col>
    <profile :dialogVisible.sync="dialogVisible" :id="this.$store.state.gid"></profile>
  </el-row>
</template>

<script>
import AdminNavBar from '@/components/AdminNavBar.vue';
import Profile from '@/components/Profile.vue';

export default {
  name: 'AdminHeader',
  components: {
    AdminNavBar,
    Profile,
  },
  data() {
    return {
      dialogVisible: false,
    };
  },
  methods: {
    commandHandler(command) {
      if (command === 'logout') {
        this.$confirm('确认登出, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }).then(() => {
          this.$message({
            type: 'success',
            message: '登出成功!',
          });
          this.$store.commit('setToken', '');
          this.$store.commit('setAuth', '');
          // window.location.reload();
          const currentUrl = window.location.href;
          // const appname = currentUrl.slice(0, currentUrl.indexOf('#'));
          // const hashparam = currentUrl.slice(currentUrl.indexOf('#') + 1);
          const appname = currentUrl.match(/http:\/\/[^/]*\//)[0];
          const serviceUrl = `${appname}admin/admin/`;
          window.location.href = `http://passport.ustc.edu.cn/logout?service=${encodeURIComponent(serviceUrl)}`;
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消登出',
          });
        });
      } else if (command === 'profile') {
        this.dialogVisible = true;
      }
    },
  },
};
</script>

<style scoped>
.header {
  height: 100%;
}

.center {
  height: 100%;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-img {
  height: 40px;
  width: 40px;
  background-size: contain;
  background-repeat: no-repeat;
}

.profile-photo {
  cursor: pointer;
}
</style>
