import Blobity from "blobity";

const blobity = new Blobity({
  color: 'rgb(125, 125, 125)',
  mode: 'normal',
  zIndex: 1,
  opacity: 0.3,
  magnetic: false,
  dotColor: '#cd6e57',
  size: 32,
  focusableElementsOffsetX: 4,
  focusableElementsOffsetY: 4,
});

blobity.switchColor = (color) => {
  blobity.updateOptions({
    dotColor: color
  })
}

export default (context, inject) => {
  context.$blobity = blobity
  inject('blobity', blobity)
}