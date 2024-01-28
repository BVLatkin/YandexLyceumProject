class SparkEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = spark_images
        self.animation_count = 0

    def main(self, display1):
        if self.animation_count >= len(self.images) * 4:
            return True

        display1.blit(self.images[self.animation_count // 4], (self.x, self.y))
        self.animation_count += 1
        return False