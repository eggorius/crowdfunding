Dropzone.autoDiscover = false;

const myDropzone = new Dropzone('#my-dropzone', {
  maxFiles: 5,
  maxFilesize: 2,
  acceptedFiles: '.jpg',
  ignoreHiddenFiles: false,
  uploadMultiple: true,
})