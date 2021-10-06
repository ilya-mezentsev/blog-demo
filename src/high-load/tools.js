const fs = require('fs')
const path = require('path')

const ARTICLES_ROOT_PATH = '/tmp/blog_demo/'

/**
 *
 * @param {any[]} arr
 * @returns {number}
 */
const randomIndex = arr => Math.floor(Math.random() * arr.length)

/**
 *
 * @param {{vars: {articles: any[], comments: any[], users: any[]}}} context
 * @param {any} events
 * @param {Function} done
 */
function setCurrentArticle(context, events, done) {
    context.vars.currentArticle = context.vars.articles[randomIndex(context.vars.articles)]
    return done()
}

/**
 *
 * @param {{vars: {articles: any[], comments: any[], users: any[]}}} context
 * @param {any} events
 * @param {Function} done
 */
function setCurrentComment(context, events, done) {
    context.vars.currentComment = context.vars.comments[randomIndex(context.vars.comments)]
    return done()
}

/**
 *
 * @param {{vars: {articles: any[], comments: any[], users: any[]}}} context
 * @param {any} events
 * @param {Function} done
 */
function setRandomArticleFilePath(context, events, done) {
    const files = fs
        .readdirSync(ARTICLES_ROOT_PATH)
        .filter(filename => /for_test_\d.txt/.test(filename))
    const randomFilePath = files[randomIndex(files)]
    if (!randomFilePath) {
        throw new Error(`Unable to find files for tests in ${ARTICLES_ROOT_PATH}`)
    }

    context.vars.randomArticleFilePath = path.join(ARTICLES_ROOT_PATH, randomFilePath)

    return done()
}

// noinspection JSUnusedGlobalSymbols
module.exports = {
    setCurrentArticle,
    setRandomArticleFilePath,
    setCurrentComment,
}
