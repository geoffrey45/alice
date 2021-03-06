<template>
  <div class="l_ rounded">
    <div class="headin">Now Playing</div>
    <div
      class="button menu rounded"
      @click="showContextMenu"
      :class="{ context_on: context_on }"
    >
      <MenuSvg />
    </div>
    <div class="separator no-border"></div>
    <div>
      <SongCard :track="queue.tracks[queue.current]" />
      <Progress />
      <HotKeys />
    </div>
  </div>
</template>

<script setup lang="ts">
import SongCard from "./SongCard.vue";
import HotKeys from "./NP/HotKeys.vue";
import Progress from "./NP/Progress.vue";
import useQStore from "../../stores/queue";
import MenuSvg from "../../assets/icons/more.svg";
import trackContext from "@/contexts/track_context";
import useContextStore from "@/stores/context";
import useModalStore from "@/stores/modal";
import useQueueStore from "@/stores/queue";
import { ContextSrc } from "@/composables/enums";

import { ref } from "vue";

const queue = useQStore();
const contextStore = useContextStore();
const context_on = ref(false);

const showContextMenu = (e: Event) => {
  e.preventDefault();
  e.stopPropagation();

  const menus = trackContext(
    queue.tracks[queue.current],
    useModalStore,
    useQueueStore
  );

  contextStore.showContextMenu(e, menus, ContextSrc.Track);
  context_on.value = true;

  contextStore.$subscribe((mutation, state) => {
    if (!state.visible) {
      context_on.value = false;
    }
  });
};
</script>
<style lang="scss">
.l_ {
  padding: 1rem;
  background-color: $primary;
  text-align: center;
  width: 100%;
  display: grid;
  position: relative;
  text-transform: capitalize;

  &:hover {
    ::-moz-range-thumb {
      height: 0.8rem;
    }

    ::-webkit-slider-thumb {
      height: 0.8rem;
    }

    ::-ms-thumb {
      height: 0.8rem;
    }
  }

  .headin {
    font-weight: bold;
    font-size: 0.9rem;
  }

  .button {
    position: absolute;
    top: $small;
    cursor: pointer;
    transition: all 200ms;
    display: flex;
    align-items: center;
    padding: $smaller;

    &:hover {
      background-color: $accent;
    }
  }

  .context_on {
    background-color: $accent;
  }

  .menu {
    right: $small;
    transform: rotate(90deg);
  }

  .art {
    width: 100%;
    aspect-ratio: 1;
    place-items: center;
    margin-bottom: $small;

    .l-image {
      height: 100%;
      width: 100%;
    }
  }

  #bitrate {
    position: absolute;
    font-size: 0.75rem;
    width: max-content;
    padding: 0.2rem 0.35rem;
    top: 14.25rem;
    left: 1.5rem;
    background-color: $black;
    border-radius: $smaller;
    box-shadow: 0rem 0rem 1rem rgba(0, 0, 0, 0.438);
  }

  .title {
    font-weight: 900;
    word-break: break-all;
  }

  .artists {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.808);

    &:hover {
      text-decoration: underline 1px !important;
    }
  }
}
</style>
