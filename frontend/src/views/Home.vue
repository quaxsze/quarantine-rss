<template>
  <div>
    <main role="main">
      <section class="jumbotron text-center">
        <div class="container">
          <h1 class="jumbotron-heading">RSS</h1>
          <p class="lead text-muted">
            <b-nav style="justify-content:center;">
              <b-nav-item
                v-for="feeds_main in feeds_mains"
                :key="feeds_main.title"
                @click="loadRSSFeed(feeds_main.id)"
                >{{ feeds_main.title }}</b-nav-item
              >
            </b-nav>
          </p>
        </div>
      </section>

      <div class="album py-5 bg-light">
        <b-container>
          <b-row>
            <b-col md="4" v-for="feed in feeds" :key="feed.title">
              <b-card
                :img-src="feed.img_src"
                img-alt="Image"
                img-top
                class="mb-4 box-shadow"
              >
                <b-card-body>
                  <b-card-text>
                    {{ feed.title }}
                  </b-card-text>
                  <div
                    class="d-flex justify-content-between align-items-center"
                  >
                    <div class="btn-group">
                      <b-button
                        size="sm"
                        variant="outline-secondary"
                        :href="feed.link"
                      >
                        Read
                      </b-button>
                    </div>
                    <small class="text-muted">{{ feed.publish_date }}</small>
                  </div>
                </b-card-body>
              </b-card>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

const BASE_URL =
  process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : ''

export default {
  name: 'Home',
  data() {
    return {
      feeds_mains: [],
      feeds: []
    }
  },
  created() {
    axios
      .get(`${BASE_URL}/api/feeds`)
      .then((data) => {
        this.feeds_mains = data.data
        console.log(this.feeds_mains)
      })
      .catch((err) => {
        console.log(err)
        return null
      })
  },
  methods: {
    loadRSSFeed(feedID) {
      axios
        .get(`${BASE_URL}/api/feeds/${feedID}`)
        .then((data) => {
          this.feeds = data.data
        })
        .catch((err) => {
          console.log(err)
          return null
        })
    }
  }
}
</script>

<style></style>
