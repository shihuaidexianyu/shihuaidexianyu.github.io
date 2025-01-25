---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "start"
  text: "wondering"
  actions:
    - theme: brand
      text: List
      link: /note/list.md
    - theme: alt
      text: About
      link: /note/about.md

---
<script setup>
import SearchBox from './components/SearchBox.vue'
</script>


<ClientOnly>
   <SearchBox/>
</ClientOnly>
