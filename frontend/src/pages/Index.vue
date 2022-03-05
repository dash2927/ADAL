<template>
  <div class="q-pa-md">
    <p class="text-h5 text-red-5">Trending</p>
    <q-carousel
      v-model="slide1"
      transition-prev="slide-right"
      transition-next="slide-left"
      swipeable
      animated
      control-color="primary"
      navigation
      padding
      arrows
      height="300px"
      class="bg-grey-1 shadow-2 rounded-borders"
    >
      <q-carousel-slide :name="1" class="column no-wrap">
        <div class="row fit justify-start items-center q-gutter-xs q-col-gutter no-wrap">
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test1.jpeg">
            <div class="absolute-bottom text-center">Food Item 1</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test2.jpeg">
            <div class="absolute-bottom text-center">Food Item 2</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test3.jpeg">
            <div class="absolute-bottom text-center">Food Item 3</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test4.jpeg">
            <div class="absolute-bottom text-center">Food Item 4</div>
          </q-img>
        </div>
      </q-carousel-slide>
      <q-carousel-slide :name="2" class="column no-wrap">
        <div class="row fit justify-start items-center q-gutter-xs q-col-gutter no-wrap">
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test5.jpeg">
            <div class="absolute-bottom text-center">Food Item 5</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test6.jpeg">
            <div class="absolute-bottom text-center">Food Item 6</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test7.jpeg">
            <div class="absolute-bottom text-center">Food Item 7</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test8.jpeg">
            <div class="absolute-bottom text-center">Food Item 8</div>
          </q-img>
        </div>
      </q-carousel-slide>
      <q-carousel-slide :name="3" class="column no-wrap">
        <div class="row fit justify-start items-center q-gutter-xs q-col-gutter no-wrap">
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test9.jpeg">
            <div class="absolute-bottom text-center">Food Item 9</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test10.jpeg">
            <div class="absolute-bottom text-center">Food Item 10</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test11.jpeg">
            <div class="absolute-bottom text-center">Food Item 11</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test12.jpeg">
            <div class="absolute-bottom text-center">Food Item 12</div>
          </q-img>
        </div>
      </q-carousel-slide>
    </q-carousel>
  </div>
  <div class="q-pa-md">
    <p class="text-h5 text-red-5">Recommended</p>
    <q-carousel
      v-model="slide2"
      transition-prev="slide-right"
      transition-next="slide-left"
      swipeable
      animated
      control-color="primary"
      navigation
      padding
      arrows
      height="300px"
      class="bg-grey-1 shadow-2 rounded-borders"
    >
      <q-carousel-slide :name="1" class="column no-wrap">
        <div class="row fit justify-start items-center q-gutter-xs q-col-gutter no-wrap">
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test1.jpeg">
            <div class="absolute-bottom text-center">Food Item 1</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test2.jpeg">
            <div class="absolute-bottom text-center">Food Item 2</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test3.jpeg">
            <div class="absolute-bottom text-center">Food Item 3</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test4.jpeg">
            <div class="absolute-bottom text-center">Food Item 4</div>
          </q-img>
        </div>
      </q-carousel-slide>
      <q-carousel-slide :name="2" class="column no-wrap">
        <div class="row fit justify-start items-center q-gutter-xs q-col-gutter no-wrap">
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test5.jpeg">
            <div class="absolute-bottom text-center">Food Item 5</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test6.jpeg">
            <div class="absolute-bottom text-center">Food Item 6</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test7.jpeg">
            <div class="absolute-bottom text-center">Food Item 7</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test8.jpeg">
            <div class="absolute-bottom text-center">Food Item 8</div>
          </q-img>
        </div>
      </q-carousel-slide>
      <q-carousel-slide :name="3" class="column no-wrap">
        <div class="row fit justify-start items-center q-gutter-xs q-col-gutter no-wrap">
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test9.jpeg">
            <div class="absolute-bottom text-center">Food Item 9</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test10.jpeg">
            <div class="absolute-bottom text-center">Food Item 10</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test11.jpeg">
            <div class="absolute-bottom text-center">Food Item 11</div>
          </q-img>
          <q-img class="rounded-borders col-3 full-height" src="~assets/images/test12.jpeg">
            <div class="absolute-bottom text-center">Food Item 12</div>
          </q-img>
        </div>
      </q-carousel-slide>
    </q-carousel>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'PageIndex',
  setup() {
    return {
      slide1: ref(1),
      slide2: ref(1)
    }
  }
})
</script>

<style lang="sass" scoped>
.my-card
  width: 100%
  max-width: 250px
</style>

