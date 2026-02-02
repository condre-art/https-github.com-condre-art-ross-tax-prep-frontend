export async function getSignedUrlOrNull(
  bucket: R2Bucket,
  key: string,
  expiresIn = 300,
): Promise<string | null> {
  if (!bucket || typeof (bucket as any).createSignedUrl !== 'function') return null;
  return bucket.createSignedUrl({ key, expiresIn });
}
