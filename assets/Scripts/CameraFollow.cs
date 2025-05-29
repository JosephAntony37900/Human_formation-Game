// ... existing code ...

void LateUpdate()
{
    // ... existing code ...
    
    // Check if player exceeds vertical limit
    if (target.position.y > maxVerticalPosition)
    {
        // Instead of teleporting, clamp the position
        Vector3 clampedPosition = target.position;
        clampedPosition.y = maxVerticalPosition;
        
        // Apply smooth movement back to limit instead of instant teleportation
        target.position = Vector3.Lerp(target.position, clampedPosition, Time.deltaTime * 5f);
        
        // Adjust velocity to prevent bouncing
        Rigidbody2D playerRb = target.GetComponent<Rigidbody2D>();
        if (playerRb != null && playerRb.velocity.y > 0)
        {
            playerRb.velocity = new Vector2(playerRb.velocity.x, 0);
        }
    }
    
    // ... existing code ...
}

// ... existing code ...