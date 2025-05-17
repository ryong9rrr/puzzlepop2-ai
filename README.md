# 퍼즐팝 AI Service

- NSFW(Not Safe For Work) : 선정적 이미지 분류
- 이미지 업스케일링

## Environment

- python3 (v3.9.6)
- fastAPI

## API

### 이미지 판별 기능

NSFW를 판별합니다.

**request**

```
HTTP /nsfw-check
Body form-data
  key : file (File)
  value : 파일
```

**response**

```
{
  "predictions": {
    "drawings": double
    "hentai": double,
    "neutral": double,
    "porn": double,
    "sexy": double,
  },
  "top_class": prediction타입("drawings", "hentai", "neutral", "porn", "sexy" 중 하나의 값),
  "nsfw": boolean
}
```
