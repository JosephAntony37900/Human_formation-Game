// ... existing code ...

void Update()
{
    // Check if player is in slime
    isInSlime = CheckIfInSlime();
    
    // Apply slime effect regardless of camera movement
    if (isInSlime)
    {
        ApplySlimeEffect();
    }
    
    // Apply jump force directly, independent of camera movement
    rb.velocity = new Vector2(rb.velocity.x, 0f); // Reset vertical velocity before applying jump
    rb.AddForce(Vector2.up * jumpForce, ForceMode2D.Impulse);
}

private void ApplySlimeEffect()
{
    // Ensure slime effect is applied regardless of camera movement
    moveSpeed = slimeSpeed;
    jumpForce = slimeJumpForce;
    
    // Apply slow effect even during camera movement
    if (rb.velocity.y > 0)
    {
        rb.velocity = new Vector2(rb.velocity.x, rb.velocity.y * 0.85f);
    }
}