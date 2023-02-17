function ubuntu {
  docker run -ti -p 80:80 -v "${PWD}:/work" ubuntu bash
}